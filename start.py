import eb_cslp

import time

from gurobipy import GRB

charging_scenarios = [1, 2, 3]
results = []
solution_status = ""
for k in range(20, 540, 40):
    for v in range(4, 40, 2):
        for n in range(8, 80, 2):
            #for scenario in charging_scenarios:
            solution_status, computation_time, total_time = eb_cslp.main(k, v, n)
            time.sleep(3)
            if solution_status == GRB.OPTIMAL:
                results.append([k, v, n, computation_time, total_time])
                break
        if solution_status == GRB.OPTIMAL: break
for entry in results:
    print(entry)