import distance
import gurobipy as gp
import matplotlib
from gurobipy import GRB

import numpy as np

# example
n = 15
v = 10
m = 50
k = 200
f = 24
theta = {1:1, 2:1, 3:2, 4:3, 5:4, 6:4, 7:5, 8:6, 9:7, 10:8, 11:9, 12:10, 13:10, 14:7, 15:10}

# SETS
N = [i for i in range(1, n+1)] # set of all possible station installation options
V = [i for i in range(1, v+1)] # set of all possible charging station physical locations
M = [i for i in range(1, m+1)] # set of all bus trips
K = [i for i in range(1, k+1)] # set of all trips that need charging
F = [i for i in range(1, f+1)] # set of charging time slots

print(N)
print(V)
print(M)
print(K)
print(F)

# Parameters
SOC = {}
for k in K:SOC[k] = 100
SOC_min = 40

rnd = np.random
rnd.seed(0)

tcK = {i: rnd.randint(10, 70) for i in K}
tyK = {i: rnd.randint(10, 70) for i in K}
tcN = {i: rnd.randint(10, 70) for i in N}
tyN = {i: rnd.randint(10, 70) for i in N}

t = {}
from scipy.spatial import distance
for k in K:
    for j in N:
        t[(k, j)] = distance.euclidean([tcK[k], tyK[k]], [tcN[j], tyN[j]])
print(t)

a = {}
for i in M:
    for j in N:
        a[(i, j)] = rnd.randint(0, 2)
print(a)

xcK = {i: rnd.randint(100, 200) for i in K}
xyK = {i: rnd.randint(100, 200) for i in K}
xcN = {i: rnd.randint(100, 200) for i in N}
xyN = {i: rnd.randint(100, 200) for i in N}

d = {}
from scipy.spatial import distance
for k in K:
    for j in N:
        d[(k, j)] = distance.euclidean([xcK[k], xyK[k]], [xcN[j], xyN[j]])
print(d)

B = 1000
b = {i: rnd.randint(100, 900) for i in N}

e = 5

tau = {k: rnd.randint(1, 24) for k in K}


# Initialize the Gurobi model
model = gp.Model()

# Variables
x = model.addVars(N, vtype=GRB.BINARY, name="xj")
q = model.addVars(K, N, vtype=GRB.BINARY, name="qkj")
u = model.addVars(K, N, F, vtype=GRB.BINARY, name="ukjf")
y = model.addVars(K, vtype=GRB.INTEGER, name="yk")

# Constraints
model.addConstrs(sum(a[i, j]*x[j] for j in N) - 1 >= 0 for i in M)
model.addConstrs(sum(t[k, j] * q[k, j] for j in N) == y[k] for k in K)
model.addConstr(sum(x[j] * b[j] for j in N) <= B)
model.addConstrs(q[k, j] <= x[j] for k in K for j in N)
model.addConstrs(sum(q[k,j] for j in N) == 1 for k in K)
# model.addConstrs(sum(sum(u[k, j, f] for f in F) for j in N) == 1 for k in K)
# model.addConstrs(sum(sum(u[k, j, f] + u[k, j, f+1] for f in F if f != 60)for j in N) == 2 for k in K)
model.addConstrs(sum(u[k, j, f] for k in K) <= 1 for j in N for f in F)
model.addConstrs((SOC[k] - e * q[k, j] * d[k, j]) >= SOC_min for k in K for j in N)
for j in N:
    for r in N:
        if theta[j] == theta[r]:
            model.addConstr(x[j] + x[r] <= 1)
model.addConstrs(u[k, j, f] >= (tau[k] + t[k,j])*q[k,j] for j in N for k in K for f in F)

model.setObjective(sum(y[k] for k in K), GRB.MINIMIZE)
model.optimize()