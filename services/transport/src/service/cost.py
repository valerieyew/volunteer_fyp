import math
import copy

# calculate costs for only one bus combination
def get_cost_of_one_bus_combi(bus_sizes_tuple, bus_durations_tuple, buses): # e.g. (27,33)
    cost = 0

    for i in range(len(bus_sizes_tuple)):
        
        for bus in buses:
            if bus_sizes_tuple[i] == bus['capacity']:
                # add the costs based on the sizes and durations of buses used
                no_of_minutes = bus_durations_tuple[i]
                no_of_hours = math.ceil(no_of_minutes / 60)
                cost += bus['price_per_hour'] * no_of_hours
                break

    return cost


# for pre-optimization
# calculate costs for only one bus combination, and also convert the bus_durations_tuple from seconds to minutes
def get_cost_and_durations_in_mins_of_one_bus_combi(bus_sizes_tuple, bus_durations_tuple, buses): # e.g. (27,33)
    cost = 0
    new_duration_in_mins = []
    
    for i in range(len(bus_sizes_tuple)):
        for bus in buses:
            if bus_sizes_tuple[i] == bus['capacity']:
                # set the new durations to be in minutes
                bus_durations_tuple[i] = math.ceil(bus_durations_tuple[i] / 60)
                new_duration_in_mins.append(bus_durations_tuple[i])

                # add the costs based on the sizes and durations of buses used
                no_of_minutes = bus_durations_tuple[i]
                no_of_hours = math.ceil(no_of_minutes / 60)
                cost += bus['price_per_hour'] * no_of_hours

    return cost, new_duration_in_mins


# for pre-optimization
# calculate costs for each of the different numbers of clusters
def get_cost_and_durations_in_mins(tsp_durations, chosen_bus_combis, buses):
    default_costs = []
    durations_in_minutes = []
    
    copy_of_durations = copy.deepcopy(tsp_durations)
    
    for i in range(len(chosen_bus_combis)):
        cost, durations_in_min = get_cost_and_durations_in_mins_of_one_bus_combi(chosen_bus_combis[i], copy_of_durations[i], buses)
            
        default_costs.append(cost)
        durations_in_minutes.append(durations_in_min)
    
    return default_costs, durations_in_minutes