import pandas as pd

def get_coords_of_single_location(coordinates, keyword):
    keyword = keyword.lower()
    search = coordinates.copy()
    search = search[search["station_name"].notna()]
    search["station_name"] = search["station_name"].str.lower()
    result = search[search["station_name"].str.contains(keyword)].iloc[0]
    return [
        result["latitude"],
        result["longitude"]
    ]