import copy
from py2opt.routefinder import RouteFinder
from time_matrix import form_matrix_from_overall_list
from IPython.utils import io

def get_tsp_permutation_and_duration_for_single_time_matrix(locations_list, matrix, faster_overall_time_matrix_list, final_venue):
    with io.capture_output() as captured:
        route_finder = RouteFinder(matrix, locations_list, iterations = 10)
        duration, route = route_finder.solve()

    if route[-1] != final_venue:
        route, duration = post_process_2_opt_results(route, duration, faster_overall_time_matrix_list, final_venue)

    return route, duration + 900      # osrm durations are too small so add another 15min to each route (not sure why)


def post_process_2_opt_results(route, duration, faster_overall_time_matrix_list, final_venue):
    best_duration = duration
    final_venue_index = route.index(final_venue)
    
    # route[index] = ["Hougang MRT Station (NE14)", "1.37129229221246", "103.892380518741"]
    # route[index][0] = "Hougang MRT Station (NE14)", which is the key for overall TM list
    best_duration -= faster_overall_time_matrix_list[route[final_venue_index][0]][route[final_venue_index + 1][0]]
    best_duration += faster_overall_time_matrix_list[route[-1][0]][route[0][0]]
    
    best_route = route[final_venue_index + 1:] + route[:final_venue_index + 1]
    
    return best_route, best_duration


# for pre-optimization
# get result from tsp library
def get_tsp_permutations_and_durations(clustered_locations_list_before_tsp, faster_overall_time_matrix_list, final_venue):
    tsps = []
    tsp_durations = []

    for i in range(len(clustered_locations_list_before_tsp)):

        tsp = []
        tsp_duration = []

        # for each of the chosen bus combi route
        for j in range(len(clustered_locations_list_before_tsp[i])):
            temp_location_list_with_final_venue = copy.deepcopy(clustered_locations_list_before_tsp[i][j])
            temp_location_list_with_final_venue.append(final_venue)
            matrix = form_matrix_from_overall_list(temp_location_list_with_final_venue, faster_overall_time_matrix_list)

            permutation, duration = get_tsp_permutation_and_duration_for_single_time_matrix(temp_location_list_with_final_venue, matrix, faster_overall_time_matrix_list, final_venue)

            tsp.append(permutation)
            tsp_duration.append(duration)

        tsps.append(tsp)
        tsp_durations.append(tsp_duration)

    print("\nTSP: Got the routes and durations for all the initial clusters.\n")
    
    return tsps, tsp_durations


def convert_one_tsp_permutation_to_location_list(no_of_locations_in_this_cluster, permutation, clustered_locations_list_before_tsp, final_venue):
    # create an array of the size of this cluster
    tsp_result_locations = [None] * no_of_locations_in_this_cluster

    # set the last destination of this route to be the destination
    tsp_result_locations[no_of_locations_in_this_cluster - 1] = final_venue

    # reverse tsp results - first destination becomes final destination, etc
    for k in range(no_of_locations_in_this_cluster - 1):
        # rhs: the full location detail
        # lhs: figure out which index to put this full location detail in the tsp result location
        tsp_result_locations[no_of_locations_in_this_cluster - permutation[k] - 1] = clustered_locations_list_before_tsp[k]
        
    return tsp_result_locations


# for pre-optimization
# to keep track of the no of ppl at each location during optimization
def build_dict_with_location_name_and_no_of_ppl(tsp_result_locations_list, data_numbers, final_venue):
    locations_with_no_of_ppl = []
    for n_cluster_no in range(len(tsp_result_locations_list)):
        n_cluster_list = []

        for this_cluster_of_n_cluster_no in range(len(tsp_result_locations_list[n_cluster_no])):
            cluster_dict = {}
            for location_no in range(len(tsp_result_locations_list[n_cluster_no][this_cluster_of_n_cluster_no])):
                # get the current location
                location = tsp_result_locations_list[n_cluster_no][this_cluster_of_n_cluster_no][location_no]
                
                # if it is not final location
                if data_numbers.get(location[0]): 
                    cluster_dict[location[0]] = data_numbers[location[0]]
                    
            n_cluster_list.append(cluster_dict)
        locations_with_no_of_ppl.append(n_cluster_list)

    return locations_with_no_of_ppl