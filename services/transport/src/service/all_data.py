# you can change the input dataset here

input_buses = [
    {
        "title": "13 Seater Type",
        "company_name": "SG Bus Charter",
        "capacity": 13,
        "price_per_hour": 55,
        "contact_number": "61234567"
    },
    {
        "title": "45 Seater Type",
        "company_name": "SG Bus Charter",
        "capacity": 45,
        "price_per_hour": 70,
        "contact_number": "61234567"
    },
    {
        "title": "23 Seater Type",
        "company_name": "SG Bus Charter",
        "capacity": 23,
        "price_per_hour": 65,
        "contact_number": "61234567"
    }
]

# sort it in ascending order of capacity
buses = sorted(input_buses, key=lambda d: d['capacity'])

# final venue
final_venue = ["Somerset MRT Station"]

# # Scenario 1: Well-clustered locations
# # 15 locations with 5 participants each
# data = [
#         ["Tuas Crescent MRT Station"],
#         ["Tuas Crescent MRT Station"],
#         ["Tuas Crescent MRT Station"],
#         ["Tuas Crescent MRT Station"],
#         ["Tuas Crescent MRT Station"],
#         ["Pioneer MRT Station"],
#         ["Pioneer MRT Station"],
#         ["Pioneer MRT Station"],
#         ["Pioneer MRT Station"],
#         ["Pioneer MRT Station"],
#         ["Chinese Garden MRT Station"],
#         ["Chinese Garden MRT Station"],
#         ["Chinese Garden MRT Station"],
#         ["Chinese Garden MRT Station"],
#         ["Chinese Garden MRT Station"],
#         ["Woodlands MRT Station"],
#         ["Woodlands MRT Station"],
#         ["Woodlands MRT Station"],
#         ["Woodlands MRT Station"],
#         ["Woodlands MRT Station"],
#         ["Admiralty MRT Station"],
#         ["Admiralty MRT Station"],
#         ["Admiralty MRT Station"],
#         ["Admiralty MRT Station"],
#         ["Admiralty MRT Station"],
#         ["Sembawang MRT Station"],
#         ["Sembawang MRT Station"],
#         ["Sembawang MRT Station"],
#         ["Sembawang MRT Station"],
#         ["Sembawang MRT Station"],
#         ["Hougang MRT Station"],
#         ["Hougang MRT Station"],
#         ["Hougang MRT Station"],
#         ["Hougang MRT Station"],
#         ["Hougang MRT Station"],
#         ["Kovan MRT Station"],
#         ["Kovan MRT Station"],
#         ["Kovan MRT Station"],
#         ["Kovan MRT Station"],
#         ["Kovan MRT Station"],
#         ["Buangkok MRT Station"],
#         ["Buangkok MRT Station"],
#         ["Buangkok MRT Station"],
#         ["Buangkok MRT Station"],
#         ["Buangkok MRT Station"],
#         ["Tampines West MRT Station"],
#         ["Tampines West MRT Station"],
#         ["Tampines West MRT Station"],
#         ["Tampines West MRT Station"],
#         ["Tampines West MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Upper Changi MRT Station"],
#         ["Upper Changi MRT Station"],
#         ["Upper Changi MRT Station"],
#         ["Upper Changi MRT Station"],
#         ["Upper Changi MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Tai Seng MRT Station"],
#         ["Tai Seng MRT Station"],
#         ["Tai Seng MRT Station"],
#         ["Tai Seng MRT Station"],
#         ["Tai Seng MRT Station"],
#         ["Ubi MRT Station"],
#         ["Ubi MRT Station"],
#         ["Ubi MRT Station"],
#         ["Ubi MRT Station"],
#         ["Ubi MRT Station"]
# ]


# # Scenario 2: Sparse locations
# # 15 locations with 5 participants each
# data = [
#         ["Tuas Link MRT Station"],
#         ["Tuas Link MRT Station"],
#         ["Tuas Link MRT Station"],
#         ["Tuas Link MRT Station"],
#         ["Tuas Link MRT Station"],
#         ["Boon Lay MRT Station"],
#         ["Boon Lay MRT Station"],
#         ["Boon Lay MRT Station"],
#         ["Boon Lay MRT Station"],
#         ["Boon Lay MRT Station"],
#         ["Bukit Gombak MRT Station"],
#         ["Bukit Gombak MRT Station"],
#         ["Bukit Gombak MRT Station"],
#         ["Bukit Gombak MRT Station"],
#         ["Bukit Gombak MRT Station"],
#         ["Bukit Panjang MRT Station"],
#         ["Bukit Panjang MRT Station"],
#         ["Bukit Panjang MRT Station"],
#         ["Bukit Panjang MRT Station"],
#         ["Bukit Panjang MRT Station"],
#         ["Yishun MRT Station"],
#         ["Yishun MRT Station"],
#         ["Yishun MRT Station"],
#         ["Yishun MRT Station"],
#         ["Yishun MRT Station"],
#         ["Bishan MRT Station"],
#         ["Bishan MRT Station"],
#         ["Bishan MRT Station"],
#         ["Bishan MRT Station"],
#         ["Bishan MRT Station"],
#         ["Newton MRT Station"],
#         ["Newton MRT Station"],
#         ["Newton MRT Station"],
#         ["Newton MRT Station"],
#         ["Newton MRT Station"],
#         ["Telok Blangah MRT Station"],
#         ["Telok Blangah MRT Station"],
#         ["Telok Blangah MRT Station"],
#         ["Telok Blangah MRT Station"],
#         ["Telok Blangah MRT Station"],
#         ["Buona Vista MRT Station"],
#         ["Buona Vista MRT Station"],
#         ["Buona Vista MRT Station"],
#         ["Buona Vista MRT Station"],
#         ["Buona Vista MRT Station"],
#         ["Chinatown MRT Station"],
#         ["Chinatown MRT Station"],
#         ["Chinatown MRT Station"],
#         ["Chinatown MRT Station"],
#         ["Chinatown MRT Station"],
#         ["Jalan Besar MRT Station"],
#         ["Jalan Besar MRT Station"],
#         ["Jalan Besar MRT Station"],
#         ["Jalan Besar MRT Station"],
#         ["Jalan Besar MRT Station"],
#         ["Boon Keng MRT Station"],
#         ["Boon Keng MRT Station"],
#         ["Boon Keng MRT Station"],
#         ["Boon Keng MRT Station"],
#         ["Boon Keng MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Mountbatten MRT Station"],
#         ["Mountbatten MRT Station"],
#         ["Mountbatten MRT Station"],
#         ["Mountbatten MRT Station"],
#         ["Mountbatten MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Tanah Merah MRT Station"]
# ]


# # Scenario 3: Sparse locations
# # 22 locations with 2 participants each, except one with 3 participants
# data = [
#         ["Tuas Link MRT Station"],
#         ["Tuas Link MRT Station"],
#         ["Tuas Link MRT Station"],
#         ["Boon Lay MRT Station"],
#         ["Boon Lay MRT Station"],
#         ["Bukit Gombak MRT Station"],
#         ["Bukit Gombak MRT Station"],
#         ["Bukit Panjang MRT Station"],
#         ["Bukit Panjang MRT Station"],
#         ["Woodlands MRT Station"],
#         ["Woodlands MRT Station"],
#         ["Sembawang MRT Station"],
#         ["Sembawang MRT Station"],
#         ["Yishun MRT Station"],
#         ["Yishun MRT Station"],
#         ["Bishan MRT Station"],
#         ["Bishan MRT Station"],
#         ["Punggol MRT Station"],
#         ["Punggol MRT Station"],
#         ["Newton MRT Station"],
#         ["Newton MRT Station"],
#         ["Telok Blangah MRT Station"],
#         ["Telok Blangah MRT Station"],
#         ["Buona Vista MRT Station"],
#         ["Buona Vista MRT Station"],
#         ["Chinatown MRT Station"],
#         ["Chinatown MRT Station"],
#         ["Downtown MRT Station"],
#         ["Downtown MRT Station"],
#         ["Jalan Besar MRT Station"],
#         ["Jalan Besar MRT Station"],
#         ["Boon Keng MRT Station"],
#         ["Boon Keng MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Macpherson MRT Station"],
#         ["Mountbatten MRT Station"],
#         ["Mountbatten MRT Station"],
#         ["Nicoll Highway MRT Station"],
#         ["Nicoll Highway MRT Station"],
#         ["Tai Seng MRT Station"],
#         ["Tai Seng MRT Station"],
#         ["Ubi MRT Station"],
#         ["Ubi MRT Station"],
#         ["Tanah Merah MRT Station"],
#         ["Tanah Merah MRT Station"]
# ]

######## the bottom two scenarios can use either the transport.ipynb or set it up such that these are generated before running of app2.py

# # Scenario 4: Randomly generate 200 locations, may have repeated ones
# # OSRM only allows a maximum of 100 unique locations
# no_of_locations = 200 

# mrt = pd.read_csv('transport/mrt.csv', low_memory=False, lineterminator='\n')
# mrt_dictionary = mrt[["station_name"]].to_dict()

# def get_random_point(mrt_dictionary, final_venue):
#     station_name = final_venue[0].lower()
#     while station_name.lower() == final_venue[0].lower():
#         random_index = random.randint(0, len(mrt) - 1)
#         station_name = f'{mrt_dictionary["station_name"][random_index]} MRT Station'

#     location_list = []
#     location_list.append(station_name)
#     return location_list

# data = [get_random_point(mrt_dictionary, final_venue) for x in range(no_of_locations)]


# # Scenario 5: Randomly generate 20 locations, may have repeated ones
#             # But this time we put 10 people at each of these locations
# # OSRM only allows a maximum of 100 unique locations
# no_of_locations = 20
# no_of_people_at_each_location = 10

# mrt = pd.read_csv('transport/mrt.csv', low_memory=False, lineterminator='\n')
# mrt_dictionary = mrt[["station_name"]].to_dict()

# data = []

# for i in range(no_of_locations):
#     # to always make sure that the while loop is entered
#     station_name = final_venue[0].lower() 
    
#     # station_name always changes, so has to lowercase it for every for loop
#     while station_name.lower() == final_venue[0].lower():
#         random_index = random.randint(0, len(mrt) - 1)
#         station_name = f'{mrt_dictionary["station_name"][random_index]} MRT Station'
    
#     for j in range(no_of_people_at_each_location):
#         location_list = []
#         location_list.append(station_name)
#         data.append(location_list)