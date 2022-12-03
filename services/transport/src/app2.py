import pandas as pd

# edit import statements based on filepath e.g. from service.all_data import buses, data, final_venue
from all_data import buses, data, final_venue
from data_processing import add_coordinates_to_locations, get_data_consolidated
from time_matrix import get_time_matrix_from_osrm, build_overall_time_matrix_list, get_faster_overall_matrix
from bus_combis import get_min_and_max_no_of_clusters, get_bus_capacities, get_bus_combis_without_sorting, get_sorted_bus_combis
from libs_adjustments import adjust_lists_for_single_cluster, processing_for_clusters_with_long_durations
from kmeans import fit_kmeans, get_clustered_locations_list_before_tsp
from tsp import get_tsp_permutations_and_durations, build_dict_with_location_name_and_no_of_ppl
from cost import get_cost_and_durations_in_mins
from overall_result import get_overall_dict_for_optimization, print_n_cluster_as_more_readable_results, \
                            print_overall_dict_as_more_readable_results, check_if_all_solutions_have_no_errors
from optimization import optimize_on_all_n_clusters_in_overall_dict, get_lowest_cost_solution, print_info_of_lowest_cost

coordinates = pd.read_csv("transport/coords.csv", low_memory=False, lineterminator='\n')
# add coordinates to the locations incl. final venue
add_coordinates_to_locations(coordinates, data, final_venue)

# get the various lists needed - data-coordinates is not used now
data_numbers, data_coordinates, data_list, data_list_with_final_venue = get_data_consolidated(data, final_venue)


total_passengers = len(data)
print("Total no. of passengers:", total_passengers)
print()
print("All locations:", data_numbers)
print("No. of locations:", len(data_numbers.keys()))
print()


# Time matrix
overall_time_matrix = get_time_matrix_from_osrm(data_coordinates, final_venue) # using dictionary of unique locations
overall_time_matrix_list = build_overall_time_matrix_list(data_list_with_final_venue, overall_time_matrix) # using list of unique locations

faster_overall_time_matrix_list = get_faster_overall_matrix(overall_time_matrix_list, data_list_with_final_venue)

# print(faster_overall_time_matrix_list['Woodlands MRT Station (NS9)']['Admiralty MRT Station (NS10)'] + \
#     faster_overall_time_matrix_list['Admiralty MRT Station (NS10)']['Sembawang MRT Station (NS11)'] + \
#         faster_overall_time_matrix_list['Sembawang MRT Station (NS11)']['Buangkok MRT Station (NE15)'] + \
#             faster_overall_time_matrix_list['Buangkok MRT Station (NE15)']['Hougang MRT Station (NE14)'] + \
#                 faster_overall_time_matrix_list['Hougang MRT Station (NE14)']['Kovan MRT Station (NE13)'] + \
#                     faster_overall_time_matrix_list['Kovan MRT Station (NE13)']['Somerset MRT Station (NS23)'])


# Bus combis
bus_capacities = get_bus_capacities(buses)
min_cluster, max_cluster = get_min_and_max_no_of_clusters(total_passengers, bus_capacities)
print('Min no. of clusters:', min_cluster)
print('Max no. of clusters:', max_cluster, "\n")
bus_combis_before_sorting_by_cost = get_bus_combis_without_sorting(min_cluster, max_cluster, total_passengers, bus_capacities)
bus_combinations = get_sorted_bus_combis(min_cluster, max_cluster, bus_combis_before_sorting_by_cost, buses)


# Kmeans lib won't be able to take in 1 as no of clusters
if_single_cluster_exist = False
if min_cluster == 1:
    if_single_cluster_exist = True
    min_cluster = 2


# Kmeans clustering
sorted_no_of_people_in_each_cluster, no_of_people_in_each_cluster, cluster_allocations_of_locations, \
    chosen_bus_combis, chosen_bus_combis_indexes, selected_cluster_sizes = \
        fit_kmeans(data, min_cluster, max_cluster, bus_combinations)

# Sort the clusters based on the no of ppl within and find the full location object for each location in the clusters
clustered_locations_list_before_tsp = get_clustered_locations_list_before_tsp(selected_cluster_sizes, cluster_allocations_of_locations, data, \
    sorted_no_of_people_in_each_cluster, no_of_people_in_each_cluster)
        

# Adjust lists for the single clusters, since they are not added during Kmeans clustering
if if_single_cluster_exist:
    adjust_lists_for_single_cluster(data_list, total_passengers, bus_capacities, clustered_locations_list_before_tsp, \
        sorted_no_of_people_in_each_cluster, chosen_bus_combis, selected_cluster_sizes)
    

# Clustering and TSP results with costs before optimization
clustered_locations_list_after_tsp, tsp_durations = get_tsp_permutations_and_durations(clustered_locations_list_before_tsp, faster_overall_time_matrix_list, final_venue)


# Adjust clusters that are more than 1.5h in duration
new_sorted_no_of_people_in_each_cluster, new_clustered_locations_list_after_tsp, new_tsp_durations, \
        new_selected_cluster_sizes, new_chosen_bus_combis = processing_for_clusters_with_long_durations( \
            sorted_no_of_people_in_each_cluster, clustered_locations_list_after_tsp, tsp_durations, \
             data_numbers, faster_overall_time_matrix_list, total_passengers, buses, bus_capacities, final_venue)


# Get costs of clusters
default_costs, tsp_durations_in_mins = get_cost_and_durations_in_mins(new_tsp_durations, new_chosen_bus_combis, buses)


# Processing before optimization of results
locations_with_no_of_ppl = build_dict_with_location_name_and_no_of_ppl(new_clustered_locations_list_after_tsp, data_numbers, final_venue)
overall_dict, cluster_keys = get_overall_dict_for_optimization(new_selected_cluster_sizes, default_costs, new_sorted_no_of_people_in_each_cluster, 
                                    new_chosen_bus_combis, tsp_durations_in_mins, locations_with_no_of_ppl,
                                    new_clustered_locations_list_after_tsp)

# Pre-optimization
print("Overall results before optimization")
# before_overall_dict = copy.deepcopy(overall_dict)
# print_overall_dict_as_more_readable_results(before_overall_dict, final_venue)
print_overall_dict_as_more_readable_results(overall_dict, final_venue)

# Optimization
optimize_on_all_n_clusters_in_overall_dict(cluster_keys, overall_dict, buses, bus_capacities, faster_overall_time_matrix_list, final_venue)

# Post-optimization
print("\nOverall results after optimization:\n")
print_overall_dict_as_more_readable_results(overall_dict, final_venue)
check_if_all_solutions_have_no_errors(overall_dict, total_passengers, data_list, buses, final_venue)

# Get lowest cost solution
lowest_cost_solution = get_lowest_cost_solution(cluster_keys, overall_dict)
print("\nLowest cost solution:")
print_n_cluster_as_more_readable_results(lowest_cost_solution, final_venue)
print_info_of_lowest_cost(lowest_cost_solution)