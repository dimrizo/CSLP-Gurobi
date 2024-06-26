# Railways and Transport Laboratory, National Technical University of Athens
# Charging Stations Location Problem for Electric Buses (EB-CSLP)
# Synthetic data creation modules based on desired k, v, n parameters values

import random

import gen_rand_coordinates
import haversine

def create_problem(k, v, n):
    """Creates the synthetic data based on input parameters."""
    # v  = 9      # Number of candidate locations for charging stations
    # n  = 18      # Number of charging options
    # k  = 20      # Number of charging lines in the problem, den epanalamvanontai
    m = 56
    f1 = 6       # Number of charging slots for SLOW chargers (i.e. medium powered)
    f2 = 12      # Number of charging slots for FAST chargers (i.e. high powered, more since they refer to smaller time intervals)

    big_M = 100000  # A big number M
    # Average bus speed for urban environments extracted from:
    # https://www.researchgate.net/publication/272687997_Energy_and_Environmental_Impacts_of_Urban_Buses_and_Passenger_Cars-Comparative_Analysis_of_Sensitivity_to_Driving_Conditions/figures?lo=1
    avg_u = 26000/60
    consumption_e = 0.00074 # in kWh/meter (apo th texnikh ekthesi "Yphresies aksiologhshs programmatos pilotikhs kyklloforias hlektrikon leoforeion"

    # Create data for EB-CSLP
    # Charging Stations (CS) -related parameters
    V = [i for i in range(1, v+1)] # set of all possible charging station physical locations
    N = [i for i in range(1, n+1)] # set of all possible station installation options

    # Theta construction for Case studies 2 & 3
    theta = {}
    quotient, remainder = divmod(n, v)

    counter_charging_options = 1
    for i in V:
        if remainder > 0:
            loop_range = quotient + 1
        else:
            loop_range = quotient

        loop_counter = counter_charging_options
        for j in range(loop_range):
            theta[loop_counter + j] = i
            counter_charging_options += 1
        remainder -= 1

    # Case study 1
    # N1 = [1, 2] # Charging option indices for SLOW chargers (hardcoded, toy network)
    # N2 = [3, 4] # Charging option indices for FAST chargers (hardcoded, toy network)
    # theta = {1: 1, 2: 2, 3: 3, 4: 4} # N -> V

    # N1, N2 construction for the 4 nodes example (toy network)
    # N1 = []
    # N2 = []
    # for i in theta:
    #     if theta[i] == 1:
    #         N1.append(i)
    #     if theta[i] == 2:
    #         N1.append(i)
    #     if theta[i] == 3:
    #         N2.append(i)
    #     if theta[i] == 4:
    #         N2.append(i)

    # Case studies 2 & 3
    N1 = N[::2] # Indices for SLOW chargers
    N2 = N[1::2] # Indices for FAST chargers

    # Case study 1: toy example: hardcoded coordinates for candidate charging stations
    # tcV = {1: 37.9733, 2: 38.0012, 3: 38.0088, 4: 37.9932}
    # tyV = {1: 23.6689, 2: 23.6737, 3: 23.7629, 4: 23.7930}

    # for case study 2: computational time experimentation
    # tcV, tyV = gen_rand_coordinates.main(v)

    # for case study 3: Municipality of Athens
    tcV = {1: 37.98062, 2: 37.97071, 3: 37.97632, 4: 37.93256, 5: 38.01174, 6: 38.09556, 7: 37.97827, 8: 37.99782, 9: 38.05431}
    tyV = {1: 23.70391, 2: 23.66778, 3: 23.6913, 4: 23.71847, 5: 23.87078, 6: 23.69189, 7: 23.68983, 8: 23.7231, 9: 23.74294}

    # print("\n")
    # print(tcV)
    # print(tyV)

    # bus-related model parameters
    M  = [i for i in range(1, m+1)] # set of all bus trips
    K  = [i for i in range(1, k+1)] # set of all trips that need charging
    SOC = {}
    for k in K:
        SOC[k] = 100 # in kWh
    SOC_min = {}
    for k in K:
        SOC_min[k] = 20  # in kWh

    # Case study 1: Bus stops coordinates hardcoded for toy bus network,
    # Comment out for start_experiments.py
    # tcK = {1:37.9718, 2:37.9812, 3:38.0355, 4:37.9828, 5:38.0455,
    #      6:37.9612, 7:38.0385, 8:38.0133,  9:37.9722, 10:37.9912, 11:38.0459}
    # tyK = {1:23.7816, 2:23.7345, 3:23.7695, 4:23.7716, 5:23.7445,
    #       6:23.7595, 7:23.7025, 8:23.71328, 9:23.75, 10:23.7355, 11:23.770}
    
    # Case study 2
    #tcK, tyK = gen_rand_coordinates.main(k)

    # Case study 3: Bus stops coordinates hardcoded for Municipality of Athens,
    # comment out for start_experiments.py
    tcK = {1: 37.98571, 2: 37.98013, 3: 37.98935, 4: 37.98159, 5: 37.99376,
           6: 37.99675, 7: 37.99756, 8: 37.99776, 9: 38.00311, 10: 37.98038}
    tyK = {1: 23.73113, 2: 23.73482, 3: 23.70895, 4: 23.70412, 5: 23.77718,
           6: 23.77888, 7: 23.69946, 8: 23.69926, 9: 23.71234, 10: 23.73539}

    # print("\n")
    # print(tcK)
    # print(tyK)

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

    print("\r") #one more print, before Gurobi output

    # Budget related
    total_B = 100000000000000
    # b = {1: 700, 2: 750, 3: 500, 4: 550, 5: 600, 6: 650, 7: 900, 8: 950}
    b = {i: (200 + random.randint(50, 1000)) for i in N}

    # time-related model parameters
    F1 = [i for i in range(1, f1+1)] # set of SLOW charging time slots
    F2 = [i for i in range(1, f2+1)] # set of FAST charging time slots
    charging_start_time = 600
    charging_time_slow = 120
    charging_time_fast = 60
    charging_start_window_1 = 120
    charging_start_window_2 = 60
    # charging_start_window_1 = charging_start_window_2 # for toy network example, comment otherwise
    charging_slots_slow = {i: (charging_start_time + (i-1) * charging_time_slow) for i in F1} # Here we assume continuous time representation. We consider that \
    charging_slots_fast = {i: (charging_start_time + (i-1) * charging_time_fast) for i in F2}  # fast charging slots to have 60 min duration and slow have 120 min.
    # tau = {i: ((i*30) + charging_start_time) for i in K}
    tau = {i: round((charging_start_time + (i*(400/k)) + random.randint(0, 200)), 1) for i in K}
    #pk = {i: (tau[i] + charging_window) for i in tau}
    P1k = {i: (tau[i] + charging_start_window_1) for i in tau}
    P2k = {i: (tau[i] + charging_start_window_2) for i in tau}

    problems = {1: {"CS":       {"V": V, "N": N, "N1": N1, "N2": N2, "theta": theta, "b": b, "tcV": tcV, "tyV": tyV},
                    "bus":      {"M": M, "K": K, "SOC": SOC, "SOC_min": SOC_min, "tcK": tcK, "tyK": tyK},
                    "time":     {"F1": F1, "F2": F2, 
                                 "charging_slots_slow": charging_slots_slow,
                                 "charging_slots_fast": charging_slots_fast,
                                 "tau": tau, "P1k": P1k, "P2k": P2k},
                    "matrices": {"a": a, "d": d, "t": t},
                    "aux":      {"big_M": big_M, "avg_u": avg_u, "consumption_e": consumption_e, "total_B": total_B}
    }}

    return problems
