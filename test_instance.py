import gurobipy as gp
from gurobipy import GRB

# Create a Gurobi Model
model = gp.Model()

# Add variables, constraints, and objective to the model (replace this with your actual model)

# Variables
x = model.addVar(vtype=GRB.CONTINUOUS, name="x")
y = model.addVar(vtype=GRB.CONTINUOUS, name="y")

# Objective
model.setObjective(x + y, GRB.MAXIMIZE)

# Constraints
model.addConstr(x + 2 * y <= 10, name="constraint1")
model.addConstr(3 * x - y <= 15, name="constraint2")

# Solve the model
model.optimize()

# Check if the optimization was successful
if model.status == GRB.OPTIMAL:
    print("Optimal solution found")

# Write the LP file
model.write("model.lp")