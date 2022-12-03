
function getTspPermutationAndDurationForSingleTimeMatrix(Argument all_locations, Argument time_matrix, Argument time_hashmap, Argument final_venue){
  
    Call the Python's py2opt RouteFinder library with all locations and the time matrix.
    
    if the last point of the returned route is not the final venue:
        Call postProcess2OptResults and return its modified route and duration.
    else:
        return the route and duration returned by the RouteFinder library.
    
end
}

function postProcess2OptResults(Argument route, Argument duration, Argument time_hashmap, Argument final_venue){

    Initialize index to the index of the final venue in route, which is a list.
    
    Initialize new_route to an empty list.
    Add all locations in route after index to the new_route. Then append the remaining locations to_new route. 
    
    Initialize substract to the travelling duration between final venue and the location at index + 1 in route, obtained from time_hashmap.
    Initialize addition to the travelling duration between the locations at the last and first indexes in route, obtained from time_hashmap.
    
    Initialize new_duration to duration - subtract + addition.
    
    return new_route and new_duration
end
}

{
initialize if_single_cluster_exist to False
if minimum number of clusters == 1:
    if if_single_cluster_exist = True
    min_cluster = 2
}
    
function adjustListsForSingleCluster(Argument all_locations, Argument total_no_of_passengers, Argument bus_capacities, 
                                    Argument locations_in_clusters_list, Argument sorted_no_of_people_in_each_cluster, 
                                    Argument chosen_bus_combis, Argument selected_cluster_sizes){
    
    // locations_in_clusters_list is a list of list
    Add all_locations as a list to the front of the locations_in_clusters_list. all_locations will act the locations for one whole cluster.
    
    // sorted_no_of_people_in_each_cluster is a list of list
    Initialize a list and append the total_no_of_passengers to it.
    Add this list to the front of the sorted_no_of_people_in_each_cluster.
    
    Add 1 to the front of the selected_cluster_sizes list.
    
    // chosen_bus_combis is a list of list
    Iterate through the bus_capacities and find the smallest bus size that can accommodate total_no_of_passengers.
    Initialize a list and append this smallest bus size to it.
    Add this list to the front of the chosen_bus_combis.

end
}


function processingForClustersWithLongDurations(Argument sorted_no_of_people_in_each_cluster, Argument clustered_locations_list_after_tsp, 
    Argument tsp_durations, Argument data_numbers, Argument time_hashmap, Argument total_passengers, Argument buses, 
    Argument bus_capacities, Argument final_venue){
    
    Initialize new_sorted_no_of_people_in_each_cluster to an empty list
    Initialize new_clustered_locations_list_after_tsp to an empty list
    Initialize new_tsp_durations = to an empty list
    
    // iterate through each cluster in each n_cluster, find if there is any cluster that takes more than 90 min
    for all n_clusters:
        Initialize n_cluster_sorted_no_of_people to an empty list
        Initialize n_cluster_locations_lists to an empty list
        Initialize n_cluster_durations to an empty list
        
        for cluster in n_cluster:
            if cluster takes more than 90 min to complete: 
                Initialize no_of_clusters_to_replace_this_cluster to the ceiling of duration / 60 min
                Initialize no_of_locations_in_each_new_cluster to the ceiling of no of locations in this cluster / no_of_clusters_to_replace_this_cluster
                
                // divide this cluster by the no of clusters to replace this cluster
                Initialize new_locations_list to an empty list
                Initialize counter to 1
                
                for location in this cluster's locations:
                    Append location to new_locations_list
                    Add 1 to counter
                    
                    if counter == no_of_locations_in_each_new_cluster or this is the last location in this cluster:
                        Append final_venue to new_locations_list if it is not already in it
                            
                        Append new_locations_list to n_cluster_locations_lists
                            
                        Find the sum of the travelling durations between the locations in new_locations_list using time_hashmap
                        Append this sum to n_cluster_durations.
                        
                        Find the total number of people in these locations using data_numbers
                        Append the total number of people to n_cluster_sorted_no_of_people

                        Reinitialize new_locations_list to an empty list
                        Reinitialize counter to 1
        
            // else just add in the original data
            else: 
                Append original locations, durations and number of people to n_cluster_locations_lists, n_cluster_durations and n_cluster_sorted_no_of_people respectively
                
        // sorting of lists for current n_cluster
        Sort n_cluster_locations_lists, n_cluster_durations and n_cluster_sorted_no_of_people based on ascending order of n_cluster_sorted_no_of_people

        // add these lists to the overall lists for all n_clusters
        Append n_cluster_locations_lists to new_clustered_locations_list_after_tsp
        Append n_cluster_durations to new_tsp_durations
        Append n_cluster_sorted_no_of_people to new_sorted_no_of_people_in_each_cluster
    
    Update selected_cluster_sizes using the length of each n_cluster_locations_lists in new_clustered_locations_list_after_tsp
    Initalize new_selected_cluster_sizes to the updated selected_cluster_sizes
    
    Update bus_combis using each n_cluster_sorted_no_of_people list in new_sorted_no_of_people_in_each_cluster
    Initalize new_bus_combis to the updated bus_combis
    
    return new_sorted_no_of_people_in_each_cluster, new_clustered_locations_list_after_tsp, new_tsp_durations, \
        new_selected_cluster_sizes, new_bus_combis
end
}


function optimizeOnAllNClustersInOverallDict(Argument n_clusters, Argument buses, Argument bus_capacities, Argument time_hashmap, Argument final_venue){
    for all n_clusters:
        Initialize done_clusters to an empty list

        Initialize check to True.
        
        // start of optimization
        while check is True:
            Initialize current_cluster to the cluster with the highest number of people in this n_cluster.
            
            if there are extra space in the bus for current cluster:
                Sort the remaining clusters based on proximity to current cluster, using average coordinates of the all the locations in the other clusters.
                for all other clusters starting from the nearest cluster:
                    
                    // Proportion - ratio of extra space in bus to the number of ppl at each location
                    Initialize proportions_of_other_cluster to a list of sorted locations in other cluster based on proportion

                    // check if any location can be transferred or split between the current and other clusters
                    Call resultIfAnyLocationCanBeTransferred function which will return a list of locations that can move from other_cluster to current_cluster, if any

                    if there are location(s) that can be transferred or split: 
                        for all these location(s):
                            if it can be split:
                                Update locations, number of people at each location, routes and durations of both current_cluster and other_cluster
                            else if it can be transferred:
                                Move all locations in other_cluster to current_cluster
                                Remove other_cluster
                                Update locations, number of people at each location, route and duration of current_cluster

                    if there are no more extra space in the bus for current cluster:
                        // no need to explore other clusters
                        break

                Append current_cluster to done_clusters
                
            else: // no more clusters to iterate through 
                Reinitialize check to False

            // stop when there is only one cluster left, since the done clusters should not be changed anymore
            if number of done clusters is one less than the number of clusters:
                Reinitialize check to False
        
        // end of optimization
        // only use optimized results if it is of lower cost than before
        Update bus sizes and total cost of this n cluster
        if total cost of optimized n_cluster is lower than the original cost:
            replace n_cluster with the optimized one
end
}

function postProcess2OptResults(Argument route, Argument duration, Argument time_hashmap, Argument final_venue){

   Initialise index to the index of the final venue in route, which is a list.
  
   Initialise new_route to an empty list.
   Add all locations in route after index to the new_route. Then append the 
   remaining locations to_new route.
  
   Initialise subtract to the travelling duration between final venue and the 
   location at index + 1 in route, obtained from time_hashmap.
   Initialise addition to the travelling duration between the locations at the 
   last and first indexes in route, obtained from time_hashmap.
  
   Initialise new_duration to duration - subtract + addition.
  
   return new_route and new_duration
end
}