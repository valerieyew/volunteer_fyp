Methods are sorted into their respective categories in the other py files.
These methods are separated into methods for pre-optimization and for optimization.

Those for pre-optimization are indicated with a comment above it - "# for pre-optimization".

Pre-optimization methods involve iterating through multiple cluster sizes, such as for scenarios with two clusters, scenarios with three clusters, etc. Each of this scenario is called n-cluster. Within each n-cluster, there can be multiple clusters. For example, 6-cluster means there are six clusters in this scenario.

The number of clusters in a n-cluster may change after optimization, such that number of clusters != n. The new number of clusters can be found in the "no_of_clusters" key in the n-cluster dictionary generated at the last step of pre-optimization as shown below.


## If you refer to app.py, here is how the program is run:

###  Prep the data:
    1) Data is inputted into all_data.py and the respective data lists and dicts are generated.
    Locations lists in the program are always of the form [["Tuas Crescent MRT Station (EW31)", "1.32102695188066", "103.649078232635"]].

    2) Time matrix list is generated based on all the locations in the data using OSRM. A faster time matrix list/dict is built for quicker search, where you can use the source and destination as keys to get the travelling duration between them right away.
    `e.g. faster_overall_time_matrix_list['Woodlands MRT Station (NS9)']['Admiralty MRT Station (NS10)']`

    3) OSRM is only called once as subsequent time matrices will be built using this time matrix list.

    To get one base case first - complete solution with routes and costs:
        1) Find the min and max number of clusters for this set of data. We call them n-clusters, where n is the number of clusters in each n-cluster.

        2) Generate possible bus combinations for each n-cluster. Then sort them based on cost, so we know when we iterate to a bus combi that can fit a n-cluster, that is the cheapest bus combi for it.

        3) If total passengers can fit in a single bus (i.e. 1-cluster), we will use a boolean to keep track of it. We will not pass into the Kmeans clustering in next step as it cannot take in 1 as number of clusters.

        4) Kmeans clustering - cluster the locations in data. It will return us for each n-cluster - which location belong in which cluster, no of ppl in each cluster, and the chosen bus combi for this n-cluster.
        If there is no bus combi for the n-cluster, it would not be in selected_cluster_sizes and hence not processed.

        5) Get the locations list in each cluster of each n-cluster.

        6) For all the lists being created in Kmeans clustering algorithm and when creating the locations list, we will add in the respective values for 1-cluster at the front of these lists, if any.

        7) These lists are used to run TSP - get the routes and durations for all clusters.

        8) Post-processing after TSP: We have to divide huge clusters that take more than 1.5 hours in travelling time. These clusters are divided into math.ceil(travelling time in seconds / 3600) clusters. The sequence of locations are kept the same, just divided into multiple clusters instead. Travelling time and number of people in each cluster are recalculated as the clusters are smaller now.

        9) We then get the costs of all the clusters in each n-cluster.

        10) Build a dictionary (dict_for_n_cluster) with all the information for all n-clusters, so it will be easier to fetch the data for optimization.

###  Optimization:
        Assumptions:
         1) Bigger buses are always cheaper.
         2) Buses are always charged by the hour.
         3) There is only one dropoff location.

        Steps for each n-cluster:
         1) Find the cluster with the largest number of people, and the extra space in their bus if any.

         2) If there is extra space, we will sort the other clusters based on their proximity to this cluster. 
         
         3) While iterating each of these other clusters in sequence, we first find the proportion of each location in them. Proportion - extra space / no of ppl in that other cluster. We will then sort these locations in the other cluster by their proportions calculated.

         3) We will try adding the location (in other cluster) with the highest proportion first. A time matrix is built from the faster_overall_time_matrix_list and sent to TSP to calculate if the current locations + new location can be traversed in less than the current duration of the current cluster. If yes, then we will add the location to the locations list to be added.

         4) In the case where the entire location can be shifted from the other cluster to the current cluster, we will do so as it will be better than splitting the location. We will split the location only if the proportion < 1.

         5) Lastly, we do the actual shifting and splitting in the dict_for_n_cluster.

         6) Then we move on to the next cluster in the n-cluster, and when all are done, to the next n-cluster, and so on.



## Python notebooks for testing

### Dataset

Download map from [data.gov.sg/national-map-line](https://data.gov.sg/dataset/national-map-line?resource_id=cdcbb2c7-f9ff-4eb2-823d-8401bb242438)

Download coordinates from [singapore-postal-codes](https://github.com/xkjyeah/singapore-postal-codes)


Put data `national-map-line-geojson.geojson` under the folder `/data`


### Resources

https://stackoverflow.com/questions/177343/map-navigation-project-how-is-road-data-generally-stored-represented

https://analyticsandintelligentsystems.wordpress.com/2016/11/13/finding-interconnected-road-segments-from-lta-speed-band-data/

https://github.com/perliedman/geojson-path-finder
