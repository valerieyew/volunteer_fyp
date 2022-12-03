from hashlib import new
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# for pre-optimization
def fit_kmeans(data, min_cluster, max_cluster, bus_combinations):
    df = pd.DataFrame(data, columns = ['mrt', 'lat', 'long'])
    df_lat_long = df.iloc[:,1:3]
    
    no_of_people_in_each_cluster = [] # to get number of people in each bus at the end
    sorted_no_of_people_in_each_cluster = [] # to get the bus combinations
    cluster_allocations_of_locations = []
    chosen_bus_combis = []
    chosen_bus_combis_indexes = []
    selected_cluster_sizes = []

    for i in range(min_cluster, max_cluster + 1):

        # all possible bus combis
        n_bus_cluster_combi = bus_combinations[i]

        # run KMeans
        clf = KMeans(n_clusters = i)
        clf.fit_predict(df_lat_long)
        clf = clf.labels_

        # get the sizes of clusters
        kmeans_pred_cluster = []
        for j in range(i):
            kmeans_pred_cluster.append(np.count_nonzero(clf == j))
        sorted_kmeans_pred_cluster = sorted(kmeans_pred_cluster)

        # find the bus combination for this cluster size and add to overall bus combis list
        for j in range(len(n_bus_cluster_combi)):
            chosen_bus_combi = n_bus_cluster_combi[j]
            if all(x < y for x, y in zip(tuple(sorted_kmeans_pred_cluster), chosen_bus_combi)):

                # if there is a suitable bus combi, add the results to their overall lists
                print('{}-mean clustering for total size of'.format(i), len(data), ":", kmeans_pred_cluster)
                sorted_no_of_people_in_each_cluster.append(sorted_kmeans_pred_cluster)
                no_of_people_in_each_cluster.append(kmeans_pred_cluster)

                print('Chosen bus combi', chosen_bus_combi)
                chosen_bus_combis.append(chosen_bus_combi)
                chosen_bus_combis_indexes.append(j)

                print('Assigned cluster for each of the {} stations'.format(len(data)), ":", clf, "\n")
                cluster_allocations_of_locations.append(clf)    

                selected_cluster_sizes.append(i)
                break

    return sorted_no_of_people_in_each_cluster, no_of_people_in_each_cluster, cluster_allocations_of_locations, \
                chosen_bus_combis, chosen_bus_combis_indexes, selected_cluster_sizes


# for pre-optimization
# clusters are sorted starting from lowest number of passengers in each n_cluster
def get_clustered_locations_list_before_tsp(selected_cluster_sizes, cluster_allocations_of_locations, data, \
                                           sorted_no_of_people_in_each_cluster, no_of_people_in_each_cluster):
    clustered_locations_list_before_tsp = []

    for i in range(len(selected_cluster_sizes)):
        cluster = {}
        for j in range(selected_cluster_sizes[i]):
            cluster[j] = []

        # adjust cluster no such that lower no means less passengers in that cluster
        cluster_allocations_of_locations[i] = adjust_cluster_no_of_cluster_allocations_of_locations( \
            cluster_allocations_of_locations[i], sorted_no_of_people_in_each_cluster[i], no_of_people_in_each_cluster[i])

        counter = 0
        for j in cluster_allocations_of_locations[i]:
            if data[counter] not in cluster[j]:
                cluster[j].append(data[counter])
            counter += 1
            
        clustered_locations_list_before_tsp.append(cluster)

    return clustered_locations_list_before_tsp


# for pre-optimization
# original: cluster_allocations_of_locations[i] = [3 3 1 1 4 4 4 0 0 2 2]
# after: cluster_allocations_of_locations[i] = [2 2 1 1 3 3 0 0 4 4 4], where cluster 0 has the least passengers
def adjust_cluster_no_of_cluster_allocations_of_locations(cluster_allocations_of_locations, \
                            sorted_no_of_people_in_each_cluster, no_of_people_in_each_cluster):
    
    new_index_list = [None] * len(no_of_people_in_each_cluster)
    
    # for each of the no_of_people, find the index in sorted_no_of_ppl and set the number in cluster allocations of locations to that index
    for i in range(len(no_of_people_in_each_cluster)):
        indexes_in_sorted_no_of_ppl = [k for k, j in enumerate(sorted_no_of_people_in_each_cluster) if j == no_of_people_in_each_cluster[i]]
        # if there are two clusters with same no of ppl, we need to take the next index
        for index in indexes_in_sorted_no_of_ppl:
            if index not in new_index_list:
                new_index_list[i] = index
                break
        
    new_cluster_allocations_of_locations = [new_index_list[i] for i in cluster_allocations_of_locations]

    return new_cluster_allocations_of_locations