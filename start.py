import eb_cslp

import time

from gurobipy import GRB

charging_scenarios = [1, 2, 3]
results = []
solution_status = ""

# Attempting problem solution for the various values of k, v, n
for k in range(20, 540, 40):
    for v in range(4, 40, 2):
        for n_1 in range(2, 30, 2):
            #for scenario in charging_scenarios:
            n = n_1*v
            solution_status, computation_time, total_time = eb_cslp.main(k, v, n)
            time.sleep(10) # freezing execution in order to understand state of program execution
            if solution_status == GRB.OPTIMAL:
                results.append([k, v, n, computation_time, total_time])
                break
        if solution_status == GRB.OPTIMAL: break

# Printing final results to CMD
for entry in results:
    print(entry)
