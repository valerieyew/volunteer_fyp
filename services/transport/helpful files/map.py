import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def extract_html_table(row):
    html = row["Description"]

    df = pd.read_html(html, index_col=0)[0]

    columns = pd.Series({
        "Street": df.loc["NAME"][0],
        "Folderpath": df.loc["FOLDERPATH"][0]
    })

    return pd.concat([
        row, columns
    ])

def plot_geojson(df, title, figsize=(5, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    df["geometry"].plot(ax=ax)
    plt.title(title)
    plt.show() 


def get_coords_by_code(coordinates, code):
    search = coordinates.copy()
    search = search[search["station_code"].notna()]
    result = search[search["station_code"] == code].iloc[0]
    return [
        result["latitude"],
        result["longitude"],
    ]
