# Railways and Transport Laboratory, National Technical University of Athens
# Charging Stations Location Problem for Electric Buses (EB-CSLP) - Athens Synthetic Example 3

import gurobipy as gp
from gurobipy import GRB

import haversine

# example
n = 8 # Number of charging options
v = 4 # Number of candidate locations for charging stations
m = 50 # Total number of bus lines in the problem
k = 10 # Number of charging lines in the problem, den epanalamvanontai
f1 = 6 # Number of charging slots for SLOW chargers (less since one charging slot occupies more hours in a day)
f2 = 12 # Number of charging slots for FAST chargers (more since they refer to smaller time intervals)
theta = {1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4} # N -> V
BigM = 10000

# SETS
N = [i for i in range(1, n+1)] # set of all possible station installation options
N1 = N[::2] # Indices for SLOW chargers
N2 = N[1::2] # Indices for FAST chargers
V = [i for i in range(1, v+1)] # set of all possible charging station physical locations
M = [i for i in range(1, m+1)] # set of all bus trips
K = [i for i in range(1, k+1)] # set of all trips that need charging
F1 = [i for i in range(1, f1+1)] # set of SLOW charging time slots
F2 = [i for i in range(1, f2+1)] # set of FAST charging time slots

# assuming continuous time reprsentation for a daily schedule 0-1440
#charging_slots_starting_times_slow = {i:(480 + i * 120) for i in F1} # Here we assume continuous time representation. We consider that \
#charging_slots_starting_times_fast = {i:(540 + i * 60) for i in F2}  # fast charging slots to have 60 min duration and slow have 120 min.
charging_slots_starting_times_slow = {i:(360 + i * 240) for i in F1} # Here we assume continuous time representation. We consider that \
charging_slots_starting_times_fast = {i:(500 + i * 100) for i in F2}  # fast charging slots to have 90 min duration and slow have 240 min.

tau = {1: 610, 2: 660, 3: 710, 4: 740, 5: 810, 6: 890, 7:910, 8:1000, 9:1010, 10:1050}
pk = {1: 680, 2: 730, 3: 780, 4: 810, 5: 880, 6: 960, 7:980, 8:1070, 9:1080, 10:1120} #xronos meta thn fortisi

print("Set N: ", N)
print("Set N1: ", N1)
print("Set N2: ", N2)
print("Set V: ", V)
print("Set M: ", M)
print("Set K: ", K)
print("Set F1: ", F1)
print("Set F2: ", F2)

print("Charging slots starting times for SLOW chargers:", charging_slots_starting_times_slow)
print("Charging slots starting times for FAST chargers:", charging_slots_starting_times_fast)
print("tau:", tau)
print("After charging time limit:", pk)

# Parameters
SOC = {}
for k in K:
    SOC[k] = 100 # in kWh
SOC_min = 20 # in kWh

tcK = {1:37.9718, 2:37.9812, 3:38.0355, 4:37.9828, 5:38.0455, 6:37.9712, 7:38.0585, 8:37.9822, 9:37.9612, 10:38.0555}
tyK = {1:23.7816, 2:23.7345, 3:23.7695, 4:23.7716, 5:23.7445, 6:23.7685, 7:23.7225, 8:23.7595, 9:23.7316, 10:23.7795}
tcV = {1:37.9733, 2:38.0012, 3:38.0088, 4:37.9932}
tyV = {1:23.6689, 2:23.6737, 3:23.7629, 4:23.7930}

# Printing coordinates
# print("\n")
# print(tcK)
# print(tyK)
# print(tcV)
# print(tyV)

# Calculating distances
d = {}
for k in K:
    for j in N:
        d[(k, j)] = haversine.main(tcK[k], tyK[k], tcV[theta[j]], tyV[theta[j]])

# Printing distances dictionary
# print("\n")
# print("Printing distances matrix in meters: ")
# for k in K:
#     for j in N:
#         print("(", k, ",", j, "):", round(d[(k, j)], 2),  end=", ")
#     print("\r")

# Average bus speed for urban environments extracted from:
# https://www.researchgate.net/publication/272687997_Energy_and_Environmental_Impacts_of_Urban_Buses_and_Passenger_Cars-Comparative_Analysis_of_Sensitivity_to_Driving_Conditions/figures?lo=1
avg_u = 26000/60

t = {}
for k in K:
    for j in N:
        t[(k, j)] = d[(k, j)] / avg_u

# Printing travel times dictionary
print("\n")
print("Printing travel times matrix in minutes: ")
for k in K:
    for j in N:
        print("(", k, ",", j, "):", round(t[(k, j)], 2),  end=", ")
    print("\r")

a = {}
for i in M:
    for j in N:
        a[(i, j)] = 1

# Printing connection feasibility matrix
# print("\n")
# print("Printing connection feasibility matrix: ")
# for k in K:
#     for j in N:
#         print("(", k, ",", j, "):", a[(k, j)],  end=", ")
#     print("\r")

B = 10000
b = {1:200, 2:850, 3:350, 4:1000, 5:400, 6:1150, 7:450, 8:1300}

consumption_e = 0.00074 # in kWh/meter (apo th texnikh ekthesi "Yphresies aksiologhshs programmatos pilotikhs kyklloforias hlektrikon leoforeion"

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
model.addConstr(sum(x[j] * b[j] for j in N) <= B) # Constraint (6)
model.addConstrs(q[k, j] <= x[j] for k in K for j in N) # Constraint (7)
model.addConstrs(sum(q[k, j] for k in K) >= x[j] for j in N) #To ensure that xj does not take value of 1 if no trip is assigned to charging station j
model.addConstrs(sum(q[k, j] for j in N) == 1 for k in K) # Constraint (8)

model.addConstrs(sum(u_slow[k, j, f] for f in F1) + sum(u_fast[k, j, f] for f in F2) <= q[k, j] for k in K for j in N) # new constraint

model.addConstrs(sum(sum(u_slow[k, j, f] for f in F1) for j in N1) + sum(sum(u_fast[k, j, f] for f in F2) for j in N2) == 1 for k in K) # New constraint (9)

model.addConstrs(sum(u_slow[k, j, f] for k in K) <= 1 for j in N1 for f in F1) # New constraint (11Α)
model.addConstrs(sum(u_fast[k, j, f] for k in K) <= 1 for j in N2 for f in F2) # New constraint (11Β)

model.addConstrs((SOC[k] - consumption_e * q[k, j] * d[k, j]) >= SOC_min for k in K for j in N) # Constraint (12)


# Constraint (13)
for j in N:
    for r in range(j, len(N)+1):
        if (j != r) & (theta[j] == theta[r]):
            model.addConstr(x[j] + x[r] <= 1)

model.addConstrs((1-u_slow[k, j, f])*BigM + u_slow[k, j, f] * charging_slots_starting_times_slow[f] >= (tau[k] + t[k, j]) * q[k, j] for k in K for j in N1 for f in F1) # Constraint (14Α)
model.addConstrs((1-u_fast[k, j, f])*BigM + u_fast[k, j, f] * charging_slots_starting_times_fast[f] >= (tau[k] + t[k, j]) * q[k, j] for k in K for j in N2 for f in F2) # Constraint (14Β)

model.addConstrs(-(1-u_slow[k, j, f])*BigM + u_slow[k, j, f] * charging_slots_starting_times_slow[f] <= (pk[k] + t[k, j]) * q[k, j] for k in K for j in N1 for f in F1) #gia na mhn fortizei poly argotera
model.addConstrs(-(1-u_fast[k, j, f])*BigM + u_fast[k, j, f] * charging_slots_starting_times_fast[f] <= (pk[k] + t[k, j]) * q[k, j] for k in K for j in N2 for f in F2) #gia na mhn fortizei poly argotera

model.setObjective(sum(y[k] for k in K), GRB.MINIMIZE)
model.optimize()

all_vars = model.getVars()
values = model.getAttr("X", all_vars)
names = model.getAttr("VarName", all_vars)

print("\r")
for name, val in zip(names, values):
    if val != 0:
        print(f"{name} = {val}")

if model.status == GRB.OPTIMAL:
    print("Optimal solution found")
