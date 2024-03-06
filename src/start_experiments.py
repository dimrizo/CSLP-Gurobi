# Railways and Transport Laboratory, National Technical University of Athens
# Charging Stations Location Problem for Electric Buses (EB-CSLP)
# Module for computational time experimentation - Calls eb_cslp and synthetic \
# data creator multiple times based several ranges for k, v, n parameters values.

import time

import eb_cslp

from gurobipy import GRB

def clean_memory(exceptions):
    # Delete variables not in exceptions
    for name in list(globals()):
        if name not in exceptions:
            del globals()[name]

def main():
    results = []
    solution_status = ""

    # Attempting problem solution for the various values of k, v, n
    dynamic_range_start_1 = 4
    dynamic_range_start_2 = 2

    for k in range(20, 2000, 40):
        for v in range(dynamic_range_start_1, 40, 2):
            for n_1 in range(dynamic_range_start_2, 30, 2):
                #for scenario in charging_scenarios:
                n = n_1 * v
                solution_status, computation_time, total_time = eb_cslp.main(k, v, n)
                time.sleep(5) # freezing execution in order to understand state of program execution

                if solution_status == GRB.OPTIMAL:
                    results.append([k, v, n, computation_time, total_time])
                    dynamic_range_start_2 = n_1
                    break

            if solution_status == GRB.OPTIMAL:
                dynamic_range_start_1 = v
                break

        print("Results: ")
        for entry in results:
            print(entry)
        clean_memory(['results', 'time', 'eb_cslp', 'GRB', 'clean_memory'])
        time.sleep(5) # freezing execution in order to understand state of program execution (debugging)

if __name__ == "__main__":
    main()
