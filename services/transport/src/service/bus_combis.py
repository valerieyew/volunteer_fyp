import math
import itertools

# for pre-optimization
def get_min_and_max_no_of_clusters(buses, data):
    bus_capacity_list = []
    for bus in buses:
        bus_capacity_list.append(bus['capacity'])
    bus_capacity_list.sort()

    passengers = len(data)
    min_cluster = math.ceil(passengers / bus_capacity_list[-1])
    max_cluster = math.ceil(passengers / bus_capacity_list[0])
    
    return min_cluster, max_cluster


# for pre-optimization
def get_bus_capacities(buses):
    bus_capacities = []
    for bus in buses:
        bus_capacities.append(bus['capacity'])
    bus_capacities.sort()
    
    return bus_capacities


# for pre-optimization
def get_min_and_max_no_of_clusters(total_passengers, bus_capacities):
    min_cluster = math.ceil(total_passengers / bus_capacities[-1])
    max_cluster = math.ceil(total_passengers / bus_capacities[0])
    
    return min_cluster, max_cluster


# for pre-optimization
def get_bus_combis_without_sorting(min_cluster, max_cluster, total_passengers, bus_capacities):
    bus_combinations_before_sorting_by_cost = {}

    for i in range(min_cluster, max_cluster + 1):
        n_cluster = i
        bus_combis_for_n_cluster = []
        for combination in itertools.combinations_with_replacement(bus_capacities, n_cluster):
            if sum(combination) > total_passengers:
                bus_combis_for_n_cluster.append(combination)

        bus_combinations_before_sorting_by_cost[i] = bus_combis_for_n_cluster
        
    return bus_combinations_before_sorting_by_cost


# for pre-optimization
# compile the cost of all the bus combis into a dict for sorting later
def get_cost_dictionary(min_cluster, max_cluster, bus_combis_before_sorting_by_cost, buses):
    cost_dictionary = {}

    for i in range(min_cluster, max_cluster + 1):
        bus_combis_for_current_n_of_cluster = bus_combis_before_sorting_by_cost[i]
        current_cost_dictionary_for_current_n_of_cluster = {}
        for j in range(len(bus_combis_for_current_n_of_cluster)):
            current_combi = bus_combis_for_current_n_of_cluster[j]
            current_cost = 0
            for current_bus_capacity in current_combi:
                for bus in buses:
                    if current_bus_capacity == bus['capacity']:
                        current_cost += bus['price_per_hour']
            current_cost_dictionary_for_current_n_of_cluster[j] = current_cost
        cost_dictionary[i] = current_cost_dictionary_for_current_n_of_cluster
                    
    return cost_dictionary


# for pre-optimization
def sort_cost_dictionary(cost_dictionary, min_cluster, max_cluster):
    sorted_cost_dictionary = {}
    for i in range(min_cluster, max_cluster + 1):
        sorted_cost_dict = sorted(cost_dictionary[i].items(), key=lambda x: x[1])
        sorted_cost_dictionary[i] = sorted_cost_dict
    return sorted_cost_dictionary


# for pre-optimization
def get_sorted_bus_combis(min_cluster, max_cluster, bus_combis_before_sorting_by_cost, buses):
    cost_dictionary = get_cost_dictionary(min_cluster, max_cluster, bus_combis_before_sorting_by_cost, buses)
    sorted_cost_dictionary = sort_cost_dictionary(cost_dictionary, min_cluster, max_cluster)
    
    bus_combinations = {}
    for i in range(min_cluster, max_cluster + 1):
        # for current_n of cluster 
        bus_combi = []
        sorted_cost_list_of_bus_combi = sorted_cost_dictionary[i]
        for index_and_cost in sorted_cost_list_of_bus_combi:
            index = index_and_cost[0]
            bus_combi.append(bus_combis_before_sorting_by_cost[i][index])

        bus_combinations[i] = bus_combi      

    return bus_combinations


# for pre-optimization
def get_bus_combi_for_one_n_cluster(no_of_clusters, sorted_no_of_people, total_passengers, buses, bus_capacities):
    
    # bus combis without sorting
    bus_combis_for_n_cluster = []
    for combination in itertools.combinations_with_replacement(bus_capacities, no_of_clusters):
        if sum(combination) > total_passengers:
            bus_combis_for_n_cluster.append(combination)
        
    # cost dictionary without sorting
    current_cost_dictionary = {}
    for i in range(len(bus_combis_for_n_cluster)):
        current_combi = bus_combis_for_n_cluster[i]
        current_cost = get_cost_of_one_bus_combination_without_duration(buses, current_combi)
        current_cost_dictionary[i] = current_cost
    
    # sort cost dictionary
    sorted_cost_dict = sorted(current_cost_dictionary.items(), key=lambda x: x[1])
    
    sorted_bus_combis = []
    for index_and_cost in sorted_cost_dict:
        index = index_and_cost[0]
        sorted_bus_combis.append(bus_combis_for_n_cluster[index])
    
    for sorted_bus_combi in sorted_bus_combis:
        if all(x < y for x, y in zip(tuple(sorted_no_of_people), sorted_bus_combi)):
            return sorted_bus_combi
        
    return None
    

# bus capacities are alraedy sorted from smallest to biggest
def get_smallest_bus_for_given_no_of_passengers(bus_capacities, no_of_passengers):
    for cap in bus_capacities:
        if no_of_passengers <= cap:
            return cap
        

# get cost of one bus combination
def get_cost_of_one_bus_combination_without_duration(buses, bus_combi):
    cost = 0
    for current_bus_capacity in bus_combi:
        for bus in buses:
            if current_bus_capacity == bus['capacity']:
                cost += bus['price_per_hour']
                break
    return cost


# get cost of one bus, taking into consideration its duration
def get_cost_of_a_bus_with_duration(bus_capacity, duration_in_min, buses):
    for bus in buses:
        if bus_capacity == bus['capacity']:
            cost = bus['price_per_hour'] * math.ceil(duration_in_min / 60)
            return cost