import json
from bus_combis import get_cost_of_a_bus_with_duration

# for pre-optimization
def get_overall_dict_for_optimization(selected_cluster_sizes, default_costs, no_of_people_in_each_cluster, 
                                     chosen_bus_combis, tsp_durations_in_mins, locations_with_no_of_ppl,
                                     tsp_result_locations_list):
    counter = 0
    overall_dict = {}
    cluster_keys = []

    for i in selected_cluster_sizes:
        key_for_n_cluster = str(i) + "-cluster"
        extra_key = 2
        while overall_dict.get(key_for_n_cluster):
            key_for_n_cluster = str(i) + "-" + str(extra_key) + "-cluster"
            extra_key += 1
            
        # store all the clusters used in this dataset
        cluster_keys.append(key_for_n_cluster)
            
        dict_for_n_cluster = {}

        # cost for all the clusters in n_cluster
        current_cost = default_costs[counter]
        dict_for_n_cluster["total_cost"] = current_cost
        dict_for_n_cluster["original_no_of_clusters"] = i
        dict_for_n_cluster["no_of_clusters"] = i

        # get details for each of the cluster
        initial_no_of_people_in_n_cluster = no_of_people_in_each_cluster[counter] # e.g. to get (27, 33)
        chosen_bus_combis_for_n_cluster = chosen_bus_combis[counter]
        durations_for_n_cluster = tsp_durations_in_mins[counter]
        locations_for_n_cluster_with_no_of_ppl = locations_with_no_of_ppl[counter]
        locations_for_n_cluster = tsp_result_locations_list[counter]
        
        dict_for_n_cluster["bus_combi"] = chosen_bus_combis_for_n_cluster

        for j in range(i):
            key_for_current_cluster = "cluster_" + str(j + 1)
            dict_for_current_cluster = {}
            dict_for_current_cluster["duration"] = durations_for_n_cluster[j]
            dict_for_current_cluster["no_of_passengers"] = initial_no_of_people_in_n_cluster[j]
            dict_for_current_cluster["bus_size"] = chosen_bus_combis_for_n_cluster[j]
            dict_for_current_cluster["locations_with_no_of_ppl"] = locations_for_n_cluster_with_no_of_ppl[j]
            dict_for_current_cluster["locations_with_coordinates"] = locations_for_n_cluster[j]
            dict_for_current_cluster["mean_coordinates_for_initial_locations_list"] = calculate_mean_coordinates_of_locations_list(locations_for_n_cluster[j])

            dict_for_n_cluster[key_for_current_cluster] = dict_for_current_cluster

        overall_dict[key_for_n_cluster] = dict_for_n_cluster

        counter += 1

    return overall_dict, cluster_keys


# print overall_dict with all possible n_cluster sizes
def print_overall_dict_as_more_readable_results(overall_dict, final_venue):
    for n_cluster_key in overall_dict.keys():
        n_cluster = overall_dict[n_cluster_key]
        print("\n-- For", n_cluster_key, "with total cost of", n_cluster["total_cost"], "bucks --")
        print_n_cluster_as_more_readable_results(n_cluster, final_venue)
        
# print individual n_cluster
def print_n_cluster_as_more_readable_results(n_cluster, final_venue):
    print("(Previous) number of clusters:", n_cluster["original_no_of_clusters"])
    print("(New) number of clusters:", n_cluster["no_of_clusters"])
    print("Bus combination used:", n_cluster["bus_combi"])
    print("Total cost:", n_cluster["total_cost"], "\n")
    
    bus_counter = 1
    for cluster_key in n_cluster.keys():
        if cluster_key != "total_cost" and cluster_key != "no_of_clusters" and cluster_key != \
                                    "original_no_of_clusters" and cluster_key != "bus_combi":
            cluster = n_cluster[cluster_key]
        
            print(cluster_key)
            print("Bus", bus_counter, "with bus size", cluster["bus_size"])
            print_cluster_as_more_readable_results(cluster, final_venue)
            
            bus_counter += 1

# print a cluster in a n_cluster
def print_cluster_as_more_readable_results(cluster, final_venue):
    print("No of passengers in this bus -", cluster["no_of_passengers"])
    print("Duration to be taken -", cluster["duration"], "min")
    
    print("Route:")
    locations_with_no_of_ppl = cluster["locations_with_no_of_ppl"]
    for location in cluster["locations_with_coordinates"][:-1]:
        print("\t", location[0],"-", locations_with_no_of_ppl[location[0]], "person(s)")
    print("\t", final_venue[0])
    print()
    
def check_if_all_solutions_have_no_errors(overall_dict, total_passengers, data_list, buses, final_venue):
    for n_cluster_key in overall_dict.keys():
        n_cluster = overall_dict[n_cluster_key]
        print("Checking", n_cluster_key, "now")
        
        # for n-cluster: check that bus combi has no None in the list
        bus_combi = n_cluster["bus_combi"]
        for bus in bus_combi:
            if bus == None:
                print("No bus in bus combination should be done. There is a cluster that has more passengers than any of the bus capacities.")
                break
        
        total_no_of_passengers_in_all_clusters = 0
        all_unique_locations_in_all_clusters = []
        total_cost = 0
        
        for cluster_key in n_cluster.keys():
            if cluster_key != "total_cost" and cluster_key != "no_of_clusters" and cluster_key != \
                                        "original_no_of_clusters" and cluster_key != "bus_combi":
                cluster = n_cluster[cluster_key]
                
                total_no_of_passengers_in_all_clusters += cluster["no_of_passengers"]
                total_cost += get_cost_of_a_bus_with_duration(cluster["bus_size"], cluster["duration"], buses)
                
                no_of_passengers_in_this_cluster = 0
                
                locations_with_no_of_ppl = cluster["locations_with_no_of_ppl"]
                for location_name in locations_with_no_of_ppl.keys():
                    if location_name not in all_unique_locations_in_all_clusters:
                        all_unique_locations_in_all_clusters.append(location_name)
                    
                    no_of_passengers_in_this_cluster += locations_with_no_of_ppl[location_name]
                    
                    # for each cluster in n-cluster: check that there is no location with zero passengers or less
                    if locations_with_no_of_ppl[location_name] <= 0:
                        print("There is a location in", cluster_key, "that has zero or less passengers.")
                
                # for each cluster in n-cluster: check that no. of passengers at all locations in a cluster == no. of passengers key of that cluster
                if no_of_passengers_in_this_cluster != cluster["no_of_passengers"]:
                    print("No of passengers in all locations of", cluster_key, "does not match its cluster's no of passengers.")
                    
                # for each cluster in n-cluster: check that locations with coordinates is one more than locations with no of ppl
                if len(locations_with_no_of_ppl.keys()) + 1 != len(cluster["locations_with_coordinates"]):
                    print("Number of locations in the", cluster_key, "dict's locations_with_coordinates and locations_with_no_of_ppl keys do not match. Check overall_dict.")
                    
                # for each cluster in n-cluster: all durations are below 90 min
                if cluster["duration"] > 90:
                    print(cluster_key, "has duration more than 90 minutes.")
                
        # for all clusters in n-cluster: check that total no. of passengers of all clusters == total_passengers
        if total_no_of_passengers_in_all_clusters != total_passengers:
            print("Number of passengers in all clusters does not match the original total number of passengers.")
        
        # for all clusters in n-cluster: check that all unique locations in the clusters + 1 are equal to data_list_with_final_venue
        if len(all_unique_locations_in_all_clusters) != len(data_list):
            print("unique locations:", all_unique_locations_in_all_clusters)
            print("unique locations size:", len(all_unique_locations_in_all_clusters))
            print('data_list:', data_list)
            print('data_list size:', len(data_list))
            print("Number of locations in all clusters does not match the original total number of locations (excluding final location).")
            
        # for all clusters in n-cluster: check that total cost of the buses with their durations == total cost of cluster
        if total_cost != n_cluster["total_cost"]:
            print("Total cost of the buses with their durations does not match the cluster's total cost.")
            
    print("All checked.")


# find average coordinates of all locations in a cluster
# so that we can find the nearest cluster later
def calculate_mean_coordinates_of_locations_list(locations_list):
    sum_of_latitudes = 0
    sum_of_longitudes = 0
    for location in locations_list:
        sum_of_latitudes += float(location[1])
        sum_of_longitudes += float(location[2])
        
    mean_coordinates = []
    mean_coordinates.append(sum_of_latitudes / len(locations_list))
    mean_coordinates.append(sum_of_longitudes / len(locations_list))
    
    return mean_coordinates


def pretty_print_dict(overall_dict):
    json_object = json.loads(json.dumps(overall_dict))
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)


# # for pre-optimization
# def print_overall_complete_solution_before_optimization(tsp_result_locations_list, default_costs, \
#                                                         chosen_bus_combis, no_of_people_in_each_cluster, tsp_durations_in_mins):
#     for i in range(len(tsp_result_locations_list)):
#         print("For", len(tsp_result_locations_list[i]), "clusters with total cost of", default_costs[i], "bucks")
#         print("Bus combination used:", chosen_bus_combis[i])
#         print()

#         counter = 0
#         for the_clusters in tsp_result_locations_list[i]:
#             print("Bus", counter + 1)
#             print("No of passengers in this bus -", no_of_people_in_each_cluster[i][counter])
#             print("Duration to be taken - ", tsp_durations_in_mins[i][counter])
#             for station in the_clusters:
#                 print(station)
#             counter += 1
#             print()
#         print("--\n")


# def format_solution_for_frontend(lowest_cost_solution, final_venue):
#     output = []

#     first_overall_results = []
#     overall_results = {}
#     overall_results["total_cost"] = lowest_cost_solution["total_cost"]
#     overall_results["no_of_clusters"] = lowest_cost_solution["no_of_clusters"]
#     overall_results["destination"] = final_venue
#     first_overall_results.append(overall_results)
#     output.append(first_overall_results)

#     second_cluster_results = []
#     for key in lowest_cost_solution.keys():
#         if key != "no_of_clusters" and key != "total_cost":
#             second_cluster_results.append(lowest_cost_solution[key])
#     output.append(second_cluster_results)
    
#     return output