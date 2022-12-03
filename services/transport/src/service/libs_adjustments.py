import copy
import math
from bus_combis import get_bus_combi_for_one_n_cluster

# for pre-optimization, after Kmeans library
# adjust lists for single cluster since Kmeans only add multi-clusters info to these three lists
def adjust_lists_for_single_cluster(data_list, total_passengers, bus_capacities, clustered_locations_list_before_tsp, \
                                    sorted_no_of_people_in_each_cluster, chosen_bus_combis, selected_cluster_sizes):
    temp_location_list = {}
    temp_location_list[0] = data_list.copy()
    clustered_locations_list_before_tsp.insert(0, temp_location_list)
    
    no_of_people = []
    no_of_people.append(total_passengers)
    sorted_no_of_people_in_each_cluster.insert(0, no_of_people)
    
    selected_cluster_sizes.insert(0, 1)
    
    for cap in bus_capacities:  # bus caps are already sorted in ascending order
        if total_passengers <= cap:
            bus_combi = []
            bus_combi.append(cap)
            chosen_bus_combis.insert(0, bus_combi)
            break


# for pre-optimization, after first run of TSP library
# this is to divide the clusters if its duration for travelling is more than 1.5 hours
def processing_for_clusters_with_long_durations(sorted_no_of_people_in_each_cluster, clustered_locations_list_after_tsp, \
    tsp_durations, data_numbers, faster_overall_time_matrix_list, total_passengers, buses, bus_capacities, final_venue):
    
    new_sorted_no_of_people_in_each_cluster = []
    new_clustered_locations_list_after_tsp = []
    new_tsp_durations = []
    
    tsp_durations_copy = copy.deepcopy(tsp_durations)
    
    # iterate through each cluster in each n_cluster, find if have any clusters that is more than 1.5h
    for i in range(len(sorted_no_of_people_in_each_cluster)):
        n_cluster_sorted_no_of_people = []
        n_cluster_locations_lists = []
        n_cluster_durations = []
        
        for j in range(len(sorted_no_of_people_in_each_cluster[i])):
            if (tsp_durations_copy[i][j] > 60 * 90): # 1.5 hours in seconds
                duration = tsp_durations_copy[i][j]
                no_of_clusters_to_replace_this_cluster = math.ceil(duration / 3600)
                
                locations_list = clustered_locations_list_after_tsp[i][j]
                
                no_of_locations = len(locations_list)
                no_of_locations_in_each_new_cluster = math.ceil(no_of_locations / no_of_clusters_to_replace_this_cluster)
                
                # divide this cluster by the no of clusters to replace this cluster
                counter = 1
                new_locations_list = []
                for location in locations_list:
                    new_locations_list.append(location)
                    counter += 1
                    
                    # if rch the size of a new cluster or rch the end of the locations list 
                    # (i.e. final venue that is not in data_numbers) --> create new cluster
                    # add new details of the new replacement clusters to the n_clusters_list
                    if counter == no_of_locations_in_each_new_cluster or location[0] not in data_numbers:
                        if final_venue not in new_locations_list:
                            new_locations_list.append(final_venue)
                            
                        # to ensure that it is not only the final venue in the location list
                        if len(new_locations_list) > 1:
                            # add the new locations list to the others in this n_cluster
                            n_cluster_locations_lists.append(copy.deepcopy(new_locations_list))
                            
                            # add the duration
                            new_duration = 0
                            for start_location_index in range(len(new_locations_list) - 1):
                                new_duration += faster_overall_time_matrix_list[new_locations_list[start_location_index][0]][new_locations_list[start_location_index + 1][0]]
                            new_duration += 600  # add 10min as OSRM values are too low
                            n_cluster_durations.append(new_duration)
                            
                            # add no of ppl
                            new_no_of_ppl = 0
                            for location in new_locations_list:
                                if data_numbers.get(location[0]):
                                    new_no_of_ppl += data_numbers[location[0]]
                            n_cluster_sorted_no_of_people.append(new_no_of_ppl)
                            
                            new_locations_list = []
                            counter = 1
        
            # else just add in the original data
            else: 
                n_cluster_sorted_no_of_people.append(sorted_no_of_people_in_each_cluster[i][j])
                n_cluster_locations_lists.append(clustered_locations_list_after_tsp[i][j])
                n_cluster_durations.append(tsp_durations[i][j])
                
        # sort all three lists based on the no of ppl in the clusters
        n_cluster_sorted_no_of_people_copy = copy.deepcopy(n_cluster_sorted_no_of_people)
        
        n_cluster_sorted_no_of_people, n_cluster_locations_lists = (list(t) for t in \
            zip(*sorted(zip(n_cluster_sorted_no_of_people, n_cluster_locations_lists))))
        
        n_cluster_sorted_no_of_people_copy, n_cluster_durations = (list(t) for t in \
            zip(*sorted(zip(n_cluster_sorted_no_of_people_copy, n_cluster_durations))))

        # add the new lists for this n_cluster to their respective lists for all clusters
        new_sorted_no_of_people_in_each_cluster.append(copy.deepcopy(n_cluster_sorted_no_of_people))
        new_clustered_locations_list_after_tsp.append(copy.deepcopy(n_cluster_locations_lists))
        new_tsp_durations.append(copy.deepcopy(n_cluster_durations))
    
    # reset selected cluster sizes by running thru the list(s)
    # chosen bus combi - get bus combi based on no of ppl in the new clusters
    new_selected_cluster_sizes = []
    new_bus_combis = []
    for n_cluster_index in range(len(new_clustered_locations_list_after_tsp)):
        no_of_clusters = len(new_clustered_locations_list_after_tsp[n_cluster_index])
        new_selected_cluster_sizes.append(no_of_clusters)
        
        sorted_no_of_people = new_sorted_no_of_people_in_each_cluster[n_cluster_index]
        bus_combi = get_bus_combi_for_one_n_cluster(no_of_clusters, sorted_no_of_people, total_passengers, buses, bus_capacities)
        if bus_combi == None:
            new_sorted_no_of_people_in_each_cluster.remove(n_cluster_index)
            new_clustered_locations_list_after_tsp.remove(n_cluster_index)
            new_tsp_durations.remove(n_cluster_index)
            new_selected_cluster_sizes.remove(n_cluster_index)
        else:
            new_bus_combis.append(bus_combi)
    
    return new_sorted_no_of_people_in_each_cluster, new_clustered_locations_list_after_tsp, new_tsp_durations, \
        new_selected_cluster_sizes, new_bus_combis