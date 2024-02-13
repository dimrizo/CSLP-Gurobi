# Railways and Transport Laboratory, National Technical University of Athens
# Charging Stations Location Problem for Electric Buses (EB-CSLP) - Module for synthetic data creation

import gen_rand_coordinates

def create_problem():
    """Creates the synthetic data based on input parameters."""
    v  = 4       # Number of candidate locations for charging stations
    n  = 4       # Number of charging options
    m  = 50      # Total number of bus lines in the problem
    k  = 5       # Number of charging lines in the problem, den epanalamvanontai
    f1 = 6       # Number of charging slots for SLOW chargers (less since one charging slot occupies more hours in a day)
    f2 = 12      # Number of charging slots for FAST chargers (more since they refer to smaller time intervals)
    charging_start_time = 600
    charging_time_slow = 120
    charging_time_fast = 60
    tau = {1: 610, 2: 660, 3: 710, 4: 740, 5: 810, 6: 890, 7:910, 8:1000, 9:1010, 10:1050}
    charging_window = 87
    big_M = 100000  # A big number M
    # Average bus speed for urban environments extracted from:
    # https://www.researchgate.net/publication/272687997_Energy_and_Environmental_Impacts_of_Urban_Buses_and_Passenger_Cars-Comparative_Analysis_of_Sensitivity_to_Driving_Conditions/figures?lo=1
    avg_u = 26000/60
    total_B = 1000000
    b = {1:700, 2:750, 3:500, 4:550, 5:600, 6:650, 7:900, 8:950}
    consumption_e = 0.00074 # in kWh/meter (apo th texnikh ekthesi "Yphresies aksiologhshs programmatos pilotikhs kyklloforias hlektrikon leoforeion"

    # Create data for EB-CSLP
    # Charging Stations (CS) -related parameters
    V  = [i for i in range(1, v+1)] # set of all possible charging station physical locations
    N  = [i for i in range(1, n+1)] # set of all possible station installation options
    N1    = [1, 2] # Charging option indices for SLOW chargers
    N2    = [3, 4] # Charging option indices for FAST chargers
    # N1 = N[::2] # Indices for SLOW chargers
    # N2 = N[1::2] # Indices for FAST chargers
    theta = {1:1, 2:2, 3:3, 4:4} # N -> V
    tcV = {}
    tyV = {}

    ###
    # We miss the calculation of random coordintes for Athens for the vectors tcV, tyV.
    ###

    tcV = {1:37.9733, 2:38.0012, 3:38.0088, 4:37.9932}
    tyV = {1:23.6689, 2:23.6737, 3:23.7629, 4:23.7930}

    # print("\n")
    # print(tcV)
    # print(tyV)

    # bus-related model parameters
    M  = [i for i in range(1, m+1)] # set of all bus trips
    K  = [i for i in range(1, k+1)] # set of all trips that need charging
    SOC = {}
    for k in K:
        SOC[k] = 100 # in kWh
    SOC_min = 20 # in kWh
    tcK = {}
    tyK = {}

    ###
    # We miss the calculation of random coordintes for Athens for the vectors tcK, tyK.
    ###

    tcK, tyK = gen_rand_coordinates.main(k)

    # tcK = {1:37.9718, 2:37.9812, 3:38.0355, 4:37.9828, 5:38.0455, 6:37.9712, 7:38.0585, 8:37.9822, 9:37.9612, 10:38.0555}
    # tyK = {1:23.7816, 2:23.7345, 3:23.7695, 4:23.7716, 5:23.7445, 6:23.7685, 7:23.7225, 8:23.7595, 9:23.7316, 10:23.7795}

    # print("\n")
    # print(tcK)
    # print(tyK)

    # time-related model parameters
    F1 = [i for i in range(1, f1+1)] # set of SLOW charging time slots
    F2 = [i for i in range(1, f2+1)] # set of FAST charging time slots
    charging_slots_slow = {i:(charging_start_time + (i-1) * charging_time_slow) for i in F1} # Here we assume continuous time representation. We consider that \
    charging_slots_fast = {i:(charging_start_time + (i-1) * charging_time_fast) for i in F2}  # fast charging slots to have 60 min duration and slow have 120 min.
    pk = {i:(tau[i] + charging_window) for i in tau}


    problems = {1: {"CS":       {"V": V, "N": N, "N1": N1, "N2": N2, "theta": theta, "b": b, "tcV": tcV, "tyV": tyV},
                    "bus":      {"M": M, "K": K, "SOC": SOC, "SOC_min": SOC_min, "tcK": tcK, "tyK": tyK},
                    "time":     {"F1": F1, "F2": F2, 
                                 "charging_slots_slow": charging_slots_slow, 
                                 "charging_slots_fast": charging_slots_fast,
                                 "tau": tau, "pk": pk},
                    "matrices": {},
                    "aux":      {"big_M": big_M, "avg_u": avg_u, "consumption_e": consumption_e, "total_B": total_B}
    }}

    return problems