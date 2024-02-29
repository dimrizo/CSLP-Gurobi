import eb_cslp

import time

from gurobipy import GRB

charging_scenarios = [1, 2, 3]
solution_status = ""
for k in range(20, 520, 40):
    for v in range(4, 40, 2):
        for n in range(8, 80, 2):
            #for scenario in charging_scenarios:
            solution_status, computation_time = eb_cslp.main(k, v, n)
            time.sleep(10)
            if solution_status == GRB.OPTIMAL: break
        if solution_status == GRB.OPTIMAL: break
