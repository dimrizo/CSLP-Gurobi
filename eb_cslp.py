# Railways and Transport Laboratory, National Technical University of Athens
# Charging Stations Location Problem for Electric Buses (EB-CSLP) - Athens Synthetic Example 4


import os
import gurobipy as gp
from gurobipy import GRB
import json
from dotenv import load_dotenv
import random

import synth_data_creator
from plot_coordinates import plot_coordinates_on_map

import time

# Load environment variables from .env file
load_dotenv()

start = time.time()

def main(k, v, n):
    execution_start = time.time()

    random.seed(10)

    MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY')

    # Calling the synthetic data creation module to get EB-CSLP problems
    problems = synth_data_creator.create_problem(k, v, n)
    # print(json.dumps(problems, indent=4))

    # Sets
    N     = problems[1]["CS"]["N"]
    N1    = problems[1]["CS"]["N1"] # Charging option indices for SLOW chargers
    N2    = problems[1]["CS"]["N2"] # Charging option indices for FAST chargers
    theta = problems[1]["CS"]["theta"]
    b     = problems[1]["CS"]["b"]

    V  = problems[1]["CS"]["V"] # set of all possible charging station physical locations
    M  = problems[1]["bus"]["M"] # set of all bus trips
    K  = problems[1]["bus"]["K"] # set of all trips that need charging
    F1 = problems[1]["time"]["F1"] # set of SLOW charging time slots
    F2 = problems[1]["time"]["F2"] # set of FAST charging time slots

    # assuming continuous time reprsentation for a daily schedule 0-1440
    charging_slots_slow = problems[1]["time"]["charging_slots_slow"] # Here we assume continuous time representation. We consider that \
    charging_slots_fast = problems[1]["time"]["charging_slots_fast"]  # fast charging slots to have 60 min duration and slow have 120 min.
    tau = problems[1]["time"]["tau"]
    #pk = problems[1]["time"]["pk"]
    P1k = problems[1]["time"]["P1k"]
    P2k = problems[1]["time"]["P2k"]

    # Parameters
    SOC = problems[1]["bus"]["SOC"]
    SOC_min = problems[1]["bus"]["SOC_min"] # in kWh

    tcV = problems[1]["CS"]["tcV"]
    tyV = problems[1]["CS"]["tyV"]
    tcK = problems[1]["bus"]["tcK"]
    tyK = problems[1]["bus"]["tyK"]

    big_M = problems[1]["aux"]["big_M"]
    avg_u = problems[1]["aux"]["avg_u"]
    consumption_e = problems[1]["aux"]["consumption_e"]
    total_B = problems[1]["aux"]["total_B"]

    a = problems[1]["matrices"]["a"]
    d = problems[1]["matrices"]["d"]
    t = problems[1]["matrices"]["t"]

    # Initialize the Gurobi model
    model = gp.Model()

    # Variables
    x = model.addVars(N, vtype=GRB.BINARY, name= "X")
    q = model.addVars(K, N, vtype=GRB.BINARY, name="Q")
    u_slow = model.addVars(K, N, F1, vtype=GRB.BINARY, name="U_slow")
    u_fast = model.addVars(K, N, F2, vtype=GRB.BINARY, name="U_fast")
    y = model.addVars(K, vtype=GRB.CONTINUOUS, name="Y")

    # Constraints
    model.addConstrs(sum(a[i, j] * x[j] for j in N) - 1 >= 0 for i in M) # Constraint (4)
    model.addConstrs(sum(t[k, j] * q[k, j] for j in N) == y[k] for k in K) # Constraint (5)
    model.addConstr(sum(x[j] * b[j] for j in N) <= total_B) # Constraint (6)
    model.addConstrs(q[k, j] <= x[j] for k in K for j in N) # Constraint (7)
    model.addConstrs(sum(q[k, j] for k in K) >= x[j] for j in N)  # Constraint (8) To ensure that xj does not take value of 1 if no trip is assigned to charging station j
    model.addConstrs(sum(q[k, j] for j in N) == 1 for k in K) # Constraint (9)
    model.addConstrs(sum(u_slow[k, j, f] for f in F1) + sum(u_fast[k, j, f] for f in F2) <= q[k, j] for k in K for j in N) # new constraint (10)
    model.addConstrs(sum(sum(u_slow[k, j, f] for f in F1) for j in N1) + sum(sum(u_fast[k, j, f] for f in F2) for j in N2) == 1 for k in K) # New constraint (11)
    model.addConstrs(sum(u_slow[k, j, f] for k in K) <= 1 for j in N1 for f in F1) # New constraint (12)
    model.addConstrs(sum(u_fast[k, j, f] for k in K) <= 1 for j in N2 for f in F2) # New constraint (13)
    model.addConstrs((SOC[k] - consumption_e * q[k, j] * d[k, j]) >= SOC_min[k] for k in K for j in N) # Constraint (14)

    # Constraint (13)
    # for j in N:
    #     for r in range(j, len(N)+1):
    #         if (j != r) & (theta[j] == theta[r]):
    #             model.addConstr(x[j] + x[r] <= 1)

    model.addConstrs((1-u_slow[k, j, f])*big_M + u_slow[k, j, f] * charging_slots_slow[f] >= (tau[k] + t[k, j]) * q[k, j] for k in K for j in N1 for f in F1) # Constraint (14Α)
    model.addConstrs((1-u_fast[k, j, f])*big_M + u_fast[k, j, f] * charging_slots_fast[f] >= (tau[k] + t[k, j]) * q[k, j] for k in K for j in N2 for f in F2) # Constraint (14Β)
    # model.addConstrs(-(1-u_slow[k, j, f])*big_M + u_slow[k, j, f] * charging_slots_slow[f] <= (pk[k] + t[k, j]) * q[k, j] for k in K for j in N1 for f in F1) #gia na mhn fortizei poly argotera
    # model.addConstrs(-(1-u_fast[k, j, f])*big_M + u_fast[k, j, f] * charging_slots_fast[f] <= (pk[k] + t[k, j]) * q[k, j] for k in K for j in N2 for f in F2) #gia na mhn fortizei poly argotera
    model.addConstrs(-(1-u_slow[k, j, f])*big_M + u_slow[k, j, f] * charging_slots_slow[f] <= (P1k[k] + t[k, j]) * q[k, j] for k in K for j in N1 for f in F1) #gia na mhn fortizei poly argotera
    model.addConstrs(-(1-u_fast[k, j, f])*big_M + u_fast[k, j, f] * charging_slots_fast[f] <= (P2k[k] + t[k, j]) * q[k, j] for k in K for j in N2 for f in F2) #gia na mhn fortizei poly argotera
    model.setObjective(sum(y[k] for k in K), GRB.MINIMIZE)

    model.optimize()

    solution_status = model.status

    if solution_status == GRB.OPTIMAL:
        print("\r")
        print("Optimal solution found")

        print("Set N: ", N)
        print("Set N1 (Slow Charging Options): ", N1)
        print("Set N2 (Fast Charging Options): ", N2)
        print("Set theta: ", theta)
        print("Set V: ", V)
        print("Set M: ", M)
        print("Set K: ", K)
        print("Set F1: ", F1)
        print("Set F2: ", F2)

        print("Charging slots starting times for SLOW chargers:", charging_slots_slow)
        print("Charging slots starting times for FAST chargers:", charging_slots_fast)
        print("tau:", tau)
        #print("After charging time limit:", pk)

        all_vars = model.getVars()
        values = model.getAttr("X", all_vars)
        names = model.getAttr("VarName", all_vars)

        # Call the function to plot coordinates for all dictionaries
        #plot_coordinates_on_map(tcK, tyK, tcV, tyV, MAPBOX_API_KEY)

        print("\r")
        for name, val in zip(names, values):
            if val != 0:
                print(f"{name} = {val}")

        print("I SOLVED a problem instance with " + str(k) + " busses, " + str(v) + " depots, and " + str(n) + " charging options.")
    else:
        print("Infeasible!!!!")
        print("I TRIED TO SOLVE a problem instance with " + str(k) + " busses, " + str(v) + " depots, and " + str(
            n) + " charging options.")

    end = time.time()
    computation_time = end-execution_start

    total_time = end - start
    return solution_status, computation_time, total_time
