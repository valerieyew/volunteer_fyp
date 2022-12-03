import math
import copy
from time_matrix import form_matrix_from_overall_list
from tsp import get_tsp_permutation_and_duration_for_single_time_matrix
from cost import get_cost_of_one_bus_combi
from optimization_sorting import get_cluster_with_next_highest_no_of_passengers, other_cluster_keys_sorted_on_proximity, \
                                    get_proportions_of_other_cluster, get_current_highest_proportion
from bus_combis import get_smallest_bus_for_given_no_of_passengers
from overall_result import pretty_print_dict

# Main function of optimization that utilizes all the other functions here
def optimize_on_all_n_clusters_in_overall_dict(cluster_keys, overall_dict, buses, bus_capacities, faster_overall_time_matrix_list, final_venue): 
    print("Names of all solutions:", cluster_keys, "\n")
    
    for n_cluster_key in cluster_keys:
        print("\nOPTIMIZATION FOR", n_cluster_key, "NOW")
        dict_for_n_cluster = copy.deepcopy(overall_dict[n_cluster_key])

        # print(n_cluster_key, "before optimization:\n")
        # print_n_cluster_as_more_readable_results(dict_for_n_cluster, final_venue)

        # keep track of finalized clusters so will not touch this cluster when splitting stations
        done_clusters = []
        all_clusters_no = list(range(1, dict_for_n_cluster["no_of_clusters"] + 1))

        # max_value will kp track of the current bus with highest no of passengers so we can get the next highest lower than it
        max_value = math.inf
        check = True
        while check == True:
            current_cluster_key, current_cluster_no, highest_no_of_passengers, extra_space_in_bus = \
                                            get_cluster_with_next_highest_no_of_passengers(dict_for_n_cluster, max_value)                   
            print("\n\nHighest no. of passengers / size of largest cluster:", highest_no_of_passengers)
            print("*** Current cluster is", current_cluster_key, "***")
            
            # if there is extra space in the bus, we will iterate through 
            # mrt stations in other clusters to see if can fit more ppl in < 1 hour
            if current_cluster_key != "" and extra_space_in_bus > 0:
                other_cluster_keys = other_cluster_keys_sorted_on_proximity(dict_for_n_cluster, current_cluster_no, current_cluster_key, done_clusters)
                # iterate through all the other clusters in this_n_cluster
                for other_cluster_key in other_cluster_keys:
                    print("\nAssessing", other_cluster_key, "(other cluster) now:")
                    
                    # calculate the ratio of extra space in bus to the no of ppl at the other cluster's locations
                    proportions_of_other_cluster = get_proportions_of_other_cluster(dict_for_n_cluster, other_cluster_key, extra_space_in_bus)
                    proportions_of_other_cluster_copy = copy.deepcopy(proportions_of_other_cluster)

                    # check if any location can be transferred or split between the current and other clusters
                    locations_list_to_be_added, location_list_of_current_cluster_new, new_duration = \
                        result_if_any_location_can_be_transferred(dict_for_n_cluster, current_cluster_key, other_cluster_key, extra_space_in_bus, \
                            proportions_of_other_cluster_copy, final_venue, faster_overall_time_matrix_list)

                    # if there are location(s) that can be transferred or split
                    if len(locations_list_to_be_added) > 0:
                        extra_space_in_bus = shift_or_split_locations_btwn_the_two_clusters(dict_for_n_cluster, current_cluster_key, location_list_of_current_cluster_new, 
                            locations_list_to_be_added, new_duration, other_cluster_key, extra_space_in_bus, faster_overall_time_matrix_list, final_venue)

                    print("Extra space in bus for", current_cluster_key, "after", other_cluster_key, ":", extra_space_in_bus)
                    if extra_space_in_bus <= 0:
                        break

                done_clusters.append(current_cluster_no)
                max_value = highest_no_of_passengers # set max value so the next loop will find the next biggest cluster
                
            else: # no more clusters to iterate through 
                check = False

            # stop when there's only one cluster left, since the other done clusters should not be changed during this optimization stage anymore
            if len(done_clusters) == len(all_clusters_no) - 1:
                check = False
            
        update_bus_sizes_and_total_cost_of_n_cluster(dict_for_n_cluster, buses, bus_capacities)
        
        if dict_for_n_cluster["total_cost"] < overall_dict[n_cluster_key]["total_cost"]:
            overall_dict[n_cluster_key] = dict_for_n_cluster
            print("Optimized", n_cluster_key, "is cheaper. Updated overall dict with optimized solution.")
            # print(n_cluster_key, "after optimization:\n")
            # print_n_cluster_as_more_readable_results(dict_for_n_cluster, final_venue)


# check if any locations can be transferred from other cluster to current cluster, or split with the latter
# if there isn't, None objects are returned with an empty array for locations to be added
def result_if_any_location_can_be_transferred(dict_for_n_cluster, current_cluster_key, other_cluster_key, extra_space_in_bus, \
                                                proportions_of_other_cluster_copy, final_venue, faster_overall_time_matrix_list):
    # copy location_list_of_current_cluster to ensure the original is not altered
    # new location list consists of locations that can be added to current cluster
    more_locations_in_other_cluster_should_be_explored = True
    
    # current cluster's duration in hours, to check later that adding a new location doesn't increase the duration
    current_no_of_hours = math.ceil(dict_for_n_cluster[current_cluster_key]["duration"] / 60)
    
    location_list_of_current_cluster_copy = copy.deepcopy(dict_for_n_cluster[current_cluster_key]["locations_with_coordinates"])
    location_list_of_current_cluster_new = None
    
    location_list_of_other_cluster = dict_for_n_cluster[other_cluster_key]["locations_with_coordinates"]
    locations_list_to_be_added = []
    
    new_duration = None
    no_of_people_added_to_current_cluster = 0

    # used a for loop here to make sure that there is an end to iteration, so actly don't need this "location"
    for location in location_list_of_other_cluster[:-1]: # final_venue is not in proportions_of_other_cluster list
        highest_proportion, index_for_location_with_highest_proportion = get_current_highest_proportion(proportions_of_other_cluster_copy)
        location_to_check = location_list_of_other_cluster[index_for_location_with_highest_proportion]
        
        if more_locations_in_other_cluster_should_be_explored and no_of_people_added_to_current_cluster < extra_space_in_bus:
            
            # copy is used to keep track of existing and added stations, so that new station can just add on to it if they fit
            if location_list_of_current_cluster_new != None:
                location_list_of_current_cluster_copy = location_list_of_current_cluster_new

            # need to add in the new location list and duration in both parameter and returned variables
            # if they are intialized within the checking method and filled up by a previous location in other cluster that be shifted completely into current cluster
            # it will iterate another location, causing these values to reinitialize to None and not include this previous location that can fit
            more_locations_in_other_cluster_should_be_explored, location_to_be_added, location_list_of_current_cluster_new, new_duration = \
                check_if_location_fit_into_current_cluster_by_duration(location_list_of_current_cluster_copy, location_list_of_current_cluster_new, \
                    new_duration, location_to_check, final_venue, current_no_of_hours, faster_overall_time_matrix_list, highest_proportion)

            if location_to_be_added != None and no_of_people_added_to_current_cluster < extra_space_in_bus:
                locations_list_to_be_added.append(location_to_be_added)
                no_of_people_added_to_current_cluster += dict_for_n_cluster[other_cluster_key]["locations_with_no_of_ppl"][location_to_check[0]]
        else:
            break
        
    return locations_list_to_be_added, location_list_of_current_cluster_new, new_duration


# iterate through other cluster's location list and return a list of locations in it
# that can fit into current cluster's location list in less than 1h
def check_if_location_fit_into_current_cluster_by_duration(location_list_of_current_cluster_copy, location_list_of_current_cluster_new, \
                                                new_duration, location_to_check, final_venue, current_no_of_hours, \
                                                faster_overall_time_matrix_list, highest_proportion):
    # get the current clusters' stations + the new one and get TSP duration
    # print("MRT stations of current cluster (initial):", location_list_of_current_cluster_copy)
    mrt_stations = copy.deepcopy(location_list_of_current_cluster_copy)
    mrt_stations.pop()
    mrt_stations.append(location_to_check)
    mrt_stations.append(final_venue)
    # print("MRT stations of current cluster (after adding", location_to_check[0], "):", mrt_stations)

    # form matrix and run TSP to get duration with new mrt station
    matrix = form_matrix_from_overall_list(mrt_stations, faster_overall_time_matrix_list)
    locations_list_new, duration = get_tsp_permutation_and_duration_for_single_time_matrix(mrt_stations, matrix, faster_overall_time_matrix_list, final_venue)

    # adjust variables to be returned whether duration is > or < than one hour
    more_locations_in_other_cluster_should_be_explored = True # explore more if this location cannot be fully shifted to or split with current cluster
    location_to_be_added = None

    # if it's the same or less number of hours as the current cluster's travel duration,
    # AND less than 1.5h (else the ride will be too long)
    new_duration_in_hours = math.ceil(math.ceil(duration / 60) / 60)
    new_duration_in_minutes = math.ceil(duration / 60)
    if new_duration_in_hours <= current_no_of_hours and new_duration_in_minutes <= 90:
        print(location_to_check, "can fit.")
        if highest_proportion < 1: # if we are already splitting one location, then no need to explore more in the same other cluster
            more_locations_in_other_cluster_should_be_explored = False
        location_to_be_added = location_to_check
        new_duration = duration
        location_list_of_current_cluster_new = locations_list_new
    else: 
        print(location_to_check, "cannot fit.")

    return more_locations_in_other_cluster_should_be_explored, location_to_be_added, location_list_of_current_cluster_new, new_duration


# shift or splitting of a location from other cluster to current cluster
def shift_or_split_locations_btwn_the_two_clusters(dict_for_n_cluster, current_cluster_key, location_list_of_current_cluster_new, locations_list_to_be_added, \
                                                    new_duration, other_cluster_key, extra_space_in_bus, faster_overall_time_matrix_list, final_venue):
    print("Shifting from", other_cluster_key, "to", current_cluster_key, "-")
    print("Locations list to be shifted:", locations_list_to_be_added)
    
    original_locations_list_in_other_cluster = copy.deepcopy(dict_for_n_cluster[other_cluster_key]["locations_with_coordinates"])
    
    # add location to current cluster
    dict_for_n_cluster[current_cluster_key]["locations_with_coordinates"] = copy.deepcopy(location_list_of_current_cluster_new)
    
    # adjust duration in current cluster
    dict_for_n_cluster[current_cluster_key]["duration"] = math.ceil(new_duration / 60)
    
    # for checking and debugging below
    current_cluster_no_of_passengers = dict_for_n_cluster[current_cluster_key]["no_of_passengers"]
    other_cluster_no_of_passengers = dict_for_n_cluster[other_cluster_key]["no_of_passengers"]
    initial_no_of_passengers_in_both_clusters = current_cluster_no_of_passengers + other_cluster_no_of_passengers
    initial_no_of_locations_in_both_clusters = len(dict_for_n_cluster[current_cluster_key]["locations_with_no_of_ppl"].keys()) + len(dict_for_n_cluster[other_cluster_key]["locations_with_no_of_ppl"].keys())
    no_of_locations_to_add_for_checking = 0
    
    # if clusters are being combined
    if len(locations_list_to_be_added) == len(original_locations_list_in_other_cluster) - 1 and other_cluster_no_of_passengers <= extra_space_in_bus:
        print("Initial extra space in bus:", extra_space_in_bus)
        print("Combining", current_cluster_key, "and", other_cluster_key, "now")
        
        # move entire other cluster into current cluster and remove other cluster
        # update no of passengers and duration
        total_no_of_ppl_in_other_cluster = dict_for_n_cluster[other_cluster_key]["no_of_passengers"]
        original_no_of_passengers = dict_for_n_cluster[current_cluster_key]["no_of_passengers"]
        dict_for_n_cluster[current_cluster_key]["no_of_passengers"] = original_no_of_passengers + total_no_of_ppl_in_other_cluster
        
        # update locations dict
        dict_for_n_cluster[current_cluster_key]["locations_with_no_of_ppl"].update(dict_for_n_cluster[other_cluster_key]["locations_with_no_of_ppl"])
        
        # remove the entire other cluster
        dict_for_n_cluster.pop(other_cluster_key)
        
        extra_space_in_bus -= total_no_of_ppl_in_other_cluster
        print("Subsequent extra space in bus:", extra_space_in_bus)
        
        # for checking and debugging below
        no_of_passengers_in_both_clusters_after_shifting = dict_for_n_cluster[current_cluster_key]["no_of_passengers"]
        no_of_locations_in_both_clusters_after_shifting = len(dict_for_n_cluster[current_cluster_key]["locations_with_no_of_ppl"].keys())

    # else if there is location(s) to be split, or only some locations from other cluster is being moved to current cluster
    else:
        for location in locations_list_to_be_added:
            if extra_space_in_bus > 0: # need to add this check as the extra space may be filled up by the location(s) in previous loop(s)
                print("Initial extra space in bus:", extra_space_in_bus)
                print("Current location being shifted:", location)
                
                # get the change in number of people in each of the affected clusters
                no_of_ppl_at_that_location = dict_for_n_cluster[other_cluster_key]["locations_with_no_of_ppl"][location[0]]
                change_in_no_of_ppl_in_both_clusters = min(extra_space_in_bus, no_of_ppl_at_that_location)
 
                # -- Current cluster --
                # add location to current cluster
                dict_for_n_cluster[current_cluster_key]["locations_with_no_of_ppl"][location[0]] = change_in_no_of_ppl_in_both_clusters

                # adjust total no of passengers in current cluster
                original_no_of_passengers = dict_for_n_cluster[current_cluster_key]["no_of_passengers"]
                dict_for_n_cluster[current_cluster_key]["no_of_passengers"] = original_no_of_passengers + change_in_no_of_ppl_in_both_clusters

                # -- Other cluster --
                # remove or split location in other cluster, in both location list and dict
                if change_in_no_of_ppl_in_both_clusters < no_of_ppl_at_that_location:
                    dict_for_n_cluster[other_cluster_key]["locations_with_no_of_ppl"][location[0]] = no_of_ppl_at_that_location - change_in_no_of_ppl_in_both_clusters
                    no_of_locations_to_add_for_checking -= 1
                elif change_in_no_of_ppl_in_both_clusters == no_of_ppl_at_that_location:
                    dict_for_n_cluster[other_cluster_key]["locations_with_no_of_ppl"].pop(location[0])
                    dict_for_n_cluster[other_cluster_key]["locations_with_coordinates"].remove(location)
                
                # adjust duration and tsp in other cluster
                locations_list_in_other_cluster = dict_for_n_cluster[other_cluster_key]["locations_with_coordinates"]
                new_matrix_for_other_cluster = form_matrix_from_overall_list(locations_list_in_other_cluster, faster_overall_time_matrix_list)
                new_locations_list_for_other_cluster, other_cluster_new_duration = get_tsp_permutation_and_duration_for_single_time_matrix(locations_list_in_other_cluster, \
                                                                            new_matrix_for_other_cluster, faster_overall_time_matrix_list, final_venue)
                dict_for_n_cluster[other_cluster_key]["duration"] = math.ceil(other_cluster_new_duration / 60)
                dict_for_n_cluster[other_cluster_key]["locations_with_coordinates"] = new_locations_list_for_other_cluster

                # adjust total no of passengers in the other cluster
                original_no_of_passengers_in_other_cluster = dict_for_n_cluster[other_cluster_key]["no_of_passengers"]
                dict_for_n_cluster[other_cluster_key]["no_of_passengers"] = original_no_of_passengers_in_other_cluster - change_in_no_of_ppl_in_both_clusters

                extra_space_in_bus -= change_in_no_of_ppl_in_both_clusters
                print("Subsequent extra space in bus:", extra_space_in_bus)
            
        # for checking and debugging below
        current_cluster_no_of_passengers_after_shifting = dict_for_n_cluster[current_cluster_key]["no_of_passengers"]
        other_cluster_no_of_passengers_after_shifting = dict_for_n_cluster[other_cluster_key]["no_of_passengers"]
        no_of_passengers_in_both_clusters_after_shifting = current_cluster_no_of_passengers_after_shifting + other_cluster_no_of_passengers_after_shifting
        no_of_locations_in_both_clusters_after_shifting = len(dict_for_n_cluster[current_cluster_key]["locations_with_no_of_ppl"].keys()) + len(dict_for_n_cluster[other_cluster_key]["locations_with_no_of_ppl"].keys()) + no_of_locations_to_add_for_checking

    # for checking and debugging if locations are not shifted correctly
    if initial_no_of_passengers_in_both_clusters != no_of_passengers_in_both_clusters_after_shifting or \
        initial_no_of_locations_in_both_clusters != no_of_locations_in_both_clusters_after_shifting:
        print("initial_no_of_passengers_in_both_clusters:", initial_no_of_passengers_in_both_clusters)
        print("no_of_passengers_in_both_clusters_after_shifting:", no_of_passengers_in_both_clusters_after_shifting)
        print("initial_no_of_locations_in_both_clusters:", initial_no_of_locations_in_both_clusters)
        print("no_of_locations_in_both_clusters_after_shifting:", no_of_locations_in_both_clusters_after_shifting)
        print("\n\nCurrent cluster key is", current_cluster_key)
        print("\n Other cluster key is", other_cluster_key)
        print(pretty_print_dict(dict_for_n_cluster))
        
        raise Exception("Locations are not shifted correctly.")
    
    return extra_space_in_bus


# check if bus sizes can be reduced and update total cost of the cluster
# update no of clusters as well
def update_bus_sizes_and_total_cost_of_n_cluster(dict_for_n_cluster, buses, bus_capacities):
    bus_sizes_list = []
    bus_durations_list = []

    no_of_cluster = dict_for_n_cluster["no_of_clusters"]
    for i in range(no_of_cluster):
        cluster_key = "cluster_" + str(i + 1)
        
        # check if cluster exists first, as it could have been combined with other clusters during shifting
        cluster = dict_for_n_cluster.get(cluster_key)
        
        if cluster:
            updated_no_of_passengers = dict_for_n_cluster[cluster_key]["no_of_passengers"]
            dict_for_n_cluster[cluster_key]["bus_size"] = get_smallest_bus_for_given_no_of_passengers(bus_capacities, updated_no_of_passengers)
            
            bus_sizes_list.append(dict_for_n_cluster[cluster_key]["bus_size"])
            bus_durations_list.append(dict_for_n_cluster[cluster_key]["duration"])
        else:
            original_quantity = dict_for_n_cluster["no_of_clusters"]
            dict_for_n_cluster["no_of_clusters"] = original_quantity - 1
    
    # update bus combi of n_cluster
    dict_for_n_cluster["bus_combi"] = bus_sizes_list

    # update cost of n_cluster
    new_total_cost = get_cost_of_one_bus_combi(bus_sizes_list, bus_durations_list, buses)
    dict_for_n_cluster["total_cost"] = new_total_cost

    
def get_lowest_cost_solution(cluster_keys, overall_dict):
    lowest_cost = math.inf
    lowest_cost_n_cluster_dict = None
    
    for n in cluster_keys:
        n_cluster_key = n
        cost_for_n_cluster = overall_dict[n_cluster_key]["total_cost"]
        
        if cost_for_n_cluster < lowest_cost:
            lowest_cost = cost_for_n_cluster
            lowest_cost_n_cluster_dict = overall_dict[n_cluster_key]
            
    return lowest_cost_n_cluster_dict
    
    
def print_info_of_lowest_cost(lowest_cost_solution):
    highest_duration = -math.inf
    lowest_cost = 0
    no_of_clusters = 0
    for cluster_key in lowest_cost_solution.keys():
        if cluster_key != "total_cost" and cluster_key != "no_of_clusters" and cluster_key != \
                                    "original_no_of_clusters" and cluster_key != "bus_combi":
            if lowest_cost_solution[cluster_key]["duration"] > highest_duration:
                highest_duration = lowest_cost_solution[cluster_key]["duration"]
        elif cluster_key == "total_cost":
            lowest_cost = lowest_cost_solution["total_cost"]
        elif cluster_key == "no_of_clusters":
            no_of_clusters = lowest_cost_solution["no_of_clusters"]
            
    print("Lowest cost:", lowest_cost)
    print("Highest duration:", highest_duration)
    print("No. of clusters:", no_of_clusters)