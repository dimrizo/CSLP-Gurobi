# Railways and Transport Laboratory, National Technical University of Athens

import gurobipy as gp
from gurobipy import GRB

import haversine

# example
n = 14
v = 7
m = 10
k = 3
f = 10
theta = {1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:5, 10:5, 11:6, 12:6, 13:7, 14:7} # N -> V

# SETS
N = [i for i in range(1, n+1)] # set of all possible station installation options
N1 = N[::2]
N2 = N[1::2]
V = [i for i in range(1, v+1)] # set of all possible charging station physical locations
M = [i for i in range(1, m+1)] # set of all bus trips
K = [i for i in range(1, k+1)] # set of all trips that need charging
F = [i for i in range(1, f+1)] # set of charging time slots
charging_slots_starting_times = {i:(540 + i * 60) for i in F}
tau = {1: 540, 2: 720, 3: 900}

print("Set N: ", N)
print("Set N1: ", N1)
print("Set N2: ", N2)
print("Set V: ", V)
print("Set M: ", M)
print("Set K: ", K)
print("Set F: ", F)

# assuming continuous time reprsentation for a daily schedule 0-1440
print("Charging_slots_starting_time:", charging_slots_starting_times)
print("tau:",tau)

# Parameters
SOC = {}
for k in K:SOC[k] = 100 # in kWh
SOC_min = 20 # in kWh

tcK = {1:37.9718, 2:37.9812, 3:38.0355}
tyK = {1:23.7816, 2:23.7345, 3:23.7695}
tcV = {1:37.9733, 2:38.0012, 3:38.0088, 4:37.9932, 5:37.9621, 6:37.9502, 7:37.9306}
tyV = {1:23.6689, 2:23.6737, 3:23.7629, 4:23.7930, 5:23.7711, 6:23.7571, 7:23.7176}

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

#Printing distances dictionary
# print("\n")
# print("Printing distances matrix in meters: ")
# for k in K:
#     for j in N:
#         print("(", k, ",", j, "):", round(d[(k, j)], 2),  end=", ")
#     print("\r")

# Average bus speed for urban environments extracted from:
# https://www.researchgate.net/publication/272687997_Energy_and_Environmental_Impacts_of_Urban_Buses_and_Passenger_Cars-Comparative_Analysis_of_Sensitivity_to_Driving_Conditions/figures?lo=1
avg_u = 26000 / 60

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

B = 1000000
b = {1:700, 2:750, 3:500, 4:550, 5:600, 6:650, 7:900, 8:950, 9:300, 10:350, 11:700, 12:750, 13:1100, 14:1150}

consumption_e = 0.00074 # in kWh/meter (apo th texnikh ekthesi "Yphresies aksiologhshs programmatos pilotikhs kyklloforias hlektrikon leoforeion"

# Initialize the Gurobi model
model = gp.Model()

# Variables
x = model.addVars(N, vtype=GRB.BINARY, name= "Xj")
q = model.addVars(K, N, vtype=GRB.BINARY, name="Qkj")
u = model.addVars(K, N, F, vtype=GRB.BINARY, name="Ukjf")
y = model.addVars(K, vtype=GRB.CONTINUOUS, name="Yk")

# Constraints
model.addConstrs(sum(a[i, j] * x[j] for j in N) - 1 >= 0 for i in M) # Constraint (4)
model.addConstrs(sum(t[k, j] * q[k, j] for j in N) == y[k] for k in K) # Constraint (5)
model.addConstr(sum(x[j] * b[j] for j in N) <= B) # Constraint (6)
model.addConstrs(q[k, j] <= x[j] for k in K for j in N) # Constraint (7)
model.addConstrs(sum(q[k, j] for j in N) == 1 for k in K) # Constraint (8)
model.addConstrs(sum(sum(u[k, j, f] for f in F) for j in N1) <= 1 for k in K) # Constraint (9)
model.addConstrs(sum(sum(u[k, j, f] for f in F) for j in N2) <= 2 for k in K) # Constraint (10)
model.addConstrs(sum(u[k, j, f] for k in K) <= 1 for j in N for f in F) # Constraint (11)
model.addConstrs((SOC[k] - consumption_e * q[k, j] * d[k, j]) >= SOC_min for k in K for j in N) # Constraint (12)
# Constraint (13)
for j in N:
    for r in range(j, len(N)+1):
        if (j != r) & (theta[j] == theta[r]):
            model.addConstr(x[j] + x[r] <= 1)
model.addConstrs(sum(u[k, j, f] * charging_slots_starting_times[f] for f in F) >= (tau[k] + t[k, j]) * q[k, j] for k in K for j in N) # Constraint (14)

model.setObjective(sum(y[k] for k in K), GRB.MINIMIZE)
model.optimize()

all_vars = model.getVars()
values = model.getAttr("X", all_vars)
names = model.getAttr("VarName", all_vars)

for name, val in zip(names, values):
    if val != 0:
        print(f"{name} = {val}")

# Write the LP file
model.write("model.lp")

if model.status == GRB.OPTIMAL:
    print("Optimal solution found")
