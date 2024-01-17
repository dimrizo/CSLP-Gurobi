# Railways and Transport Laboratory, National Technical University of Athens

import gurobipy as gp
from gurobipy import GRB

import numpy as np
from scipy.spatial import distance

import haversine

# example
n = 14
v = 7
m = 10
k = 3
f = 19
theta = {1:1, 2:1, 3:2, 4:3, 5:4, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:10, 14:7, 15:10}

# SETS
N = [i for i in range(1, n+1)] # set of all possible station installation options
V = [i for i in range(1, v+1)] # set of all possible charging station physical locations
M = [i for i in range(1, m+1)] # set of all bus trips
K = [i for i in range(1, k+1)] # set of all trips that need charging
F = [i for i in range(1, f+1)] # set of charging time slots

print("Set N: ", N)
print("Set V: ", V)
print("Set M: ", M)
print("Set K: ", K)
print("Set F: ", F)

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
    for j in V:
        d[(k, j)] = haversine.main(tcK[k], tyK[k], tcV[j], tyV[j])

#Printing distances dictionary
print("\n")
for entry in d:
    print(entry, d[entry])

u = 26000/ 60 # https://www.researchgate.net/publication/272687997_Energy_and_Environmental_Impacts_of_Urban_Buses_and_Passenger_Cars-Comparative_Analysis_of_Sensitivity_to_Driving_Conditions/figures?lo=1


t = {}
from scipy.spatial import distance
for k in K:
    for j in V:
        t[(k, j)] = d[(k, j)]/ u

#Printing distances dictionary
print("\n")
for entry in t:
    print(entry, t[entry])

a = {}
for i in M:
    for j in V:
        a[(i, j)] = 1

#Printing distances dictionary
print("\n")
for entry in a:
    print(entry, a[entry])

# xcK = {i: rnd.randint(100, 200) for i in K}
# xyK = {i: rnd.randint(100, 200) for i in K}
# xcN = {i: rnd.randint(100, 200) for i in N}
# xyN = {i: rnd.randint(100, 200) for i in N}



# B = 1000
# b = {i: rnd.randint(100, 900) for i in N}

# e = 5

# tau = {k: rnd.randint(1, 24) for k in K}


# # Initialize the Gurobi model
# model = gp.Model()

# # Variables
# x = model.addVars(N, vtype=GRB.BINARY, name="xj")
# q = model.addVars(K, N, vtype=GRB.BINARY, name="qkj")
# u = model.addVars(K, N, F, vtype=GRB.BINARY, name="ukjf")
# y = model.addVars(K, vtype=GRB.INTEGER, name="yk")

# # Constraints
# model.addConstrs(sum(a[i, j]*x[j] for j in N) - 1 >= 0 for i in M)
# model.addConstrs(sum(t[k, j] * q[k, j] for j in N) == y[k] for k in K)
# model.addConstr(sum(x[j] * b[j] for j in N) <= B)
# model.addConstrs(q[k, j] <= x[j] for k in K for j in N)
# model.addConstrs(sum(q[k,j] for j in N) == 1 for k in K)
# # model.addConstrs(sum(sum(u[k, j, f] for f in F) for j in N) == 1 for k in K)
# # model.addConstrs(sum(sum(u[k, j, f] + u[k, j, f+1] for f in F if f != 60)for j in N) == 2 for k in K)
# model.addConstrs(sum(u[k, j, f] for k in K) <= 1 for j in N for f in F)
# model.addConstrs((SOC[k] - e * q[k, j] * d[k, j]) >= SOC_min for k in K for j in N)
# for j in N:
#     for r in N:
#         if theta[j] == theta[r]:
#             model.addConstr(x[j] + x[r] <= 1)
# model.addConstrs(u[k, j, f] >= (tau[k] + t[k,j])*q[k,j] for j in N for k in K for f in F)

# model.setObjective(sum(y[k] for k in K), GRB.MINIMIZE)
# model.optimize()