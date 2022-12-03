import math

### This class consists of sorting methods used by optimization.py.

# return info on the cluster/bus with most number of passengers under max_value
def get_cluster_with_next_highest_no_of_passengers(dict_for_n_cluster, max_value):
    counter = 1

    highest_no_of_passengers = -math.inf
    cluster_key_with_highest_no_of_passengers = "" 
    cluster_no_with_highest_no_of_passengers = counter # cluster no start from 1 instead of 0
    extra_space_in_bus = 0

    for i in range(dict_for_n_cluster["no_of_clusters"]):
        cluster_key = "cluster_" + str(counter)
        
        # check if cluster exists first, as it could have been combined with other clusters during shifting
        cluster = dict_for_n_cluster.get(cluster_key)
        
        if cluster:
            no_of_passengers = dict_for_n_cluster[cluster_key]["no_of_passengers"]

            if no_of_passengers > highest_no_of_passengers and no_of_passengers < max_value:
                highest_no_of_passengers = no_of_passengers
                cluster_key_with_highest_no_of_passengers = cluster_key
                cluster_no_with_highest_no_of_passengers = counter
                extra_space_in_bus = dict_for_n_cluster[cluster_key_with_highest_no_of_passengers]["bus_size"] - highest_no_of_passengers

        counter += 1

    return cluster_key_with_highest_no_of_passengers, cluster_no_with_highest_no_of_passengers, highest_no_of_passengers, extra_space_in_bus

# sort the other clusters based on proximity to current cluster
# current cluster will iterate through the returned list of other clusters' keys
# first key will be the key of the cluster that is nearest to current cluster
def other_cluster_keys_sorted_on_proximity(dict_for_n_cluster, current_cluster_no, current_cluster_key, done_clusters):
    list_of_other_cluster_keys = []
    list_of_distance_btwn_mean_coordinates = []
    
    current_cluster_mean_coordinates = dict_for_n_cluster[current_cluster_key]["mean_coordinates_for_initial_locations_list"]
    for i in range(1, dict_for_n_cluster["no_of_clusters"] + 1):
        # so that we won't iterate through the same cluster as the current one
        if i != current_cluster_no and i not in done_clusters:
            other_cluster_key = "cluster_" + str(i)
            # check if cluster exists first, as it could have been combined with other clusters during shifting
            cluster = dict_for_n_cluster.get(other_cluster_key)
            
            if cluster:
                other_cluster_mean_coordinates = dict_for_n_cluster[other_cluster_key]["mean_coordinates_for_initial_locations_list"]
                distance = get_distance_btwn_two_coordinates(current_cluster_mean_coordinates, other_cluster_mean_coordinates)
                list_of_other_cluster_keys.append(other_cluster_key)
                list_of_distance_btwn_mean_coordinates.append(distance)

    if len(list_of_other_cluster_keys) != 0:
        list_of_distance_btwn_mean_coordinates, list_of_other_cluster_keys = (list(t) for t in \
                                    zip(*sorted(zip(list_of_distance_btwn_mean_coordinates, list_of_other_cluster_keys))))
    print("list_of_other_cluster_keys to iterate in sequence:", list_of_other_cluster_keys)

    return list_of_other_cluster_keys


def get_distance_btwn_two_coordinates(first_coord, second_coord):
    return math.sqrt((first_coord[0] - second_coord[0])**2 + (first_coord[1] - second_coord[1]) ** 2)


# iterate through the locations list and get the proportion of extra space in bus over no of ppl at each location
# for e.g. if proportion > 1: the entire location in the other cluster can be fit into the current cluster's bus
# otherwise we want to move the one with the highest proportion over too
def get_proportions_of_other_cluster(dict_for_n_cluster, other_cluster_key, extra_space_in_bus):
    proportions_of_other_cluster = []
    locations_with_no_of_ppl_in_other_cluster = dict_for_n_cluster[other_cluster_key]["locations_with_no_of_ppl"]
    locations_list_in_other_cluster = dict_for_n_cluster[other_cluster_key]["locations_with_coordinates"]
    
    for location in locations_list_in_other_cluster[:-1]:
        no_of_ppl_in_location = locations_with_no_of_ppl_in_other_cluster[location[0]]
        proportion = extra_space_in_bus / no_of_ppl_in_location
        proportions_of_other_cluster.append(proportion)

    return proportions_of_other_cluster


def get_current_highest_proportion(proportions_of_other_cluster_copy):
    # choose the location with the highest proportion
    highest_proportion = -math.inf
    index_for_location_with_highest_proportion = -1

    for index in range(len(proportions_of_other_cluster_copy)):
        if proportions_of_other_cluster_copy[index] != None and proportions_of_other_cluster_copy[index] > highest_proportion:
            highest_proportion = proportions_of_other_cluster_copy[index]
            index_for_location_with_highest_proportion = index
    
    proportions_of_other_cluster_copy[index_for_location_with_highest_proportion] = None
    return highest_proportion, index_for_location_with_highest_proportion