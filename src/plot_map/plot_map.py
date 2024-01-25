import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from data_map import coords_all_stores, coords_scraped_stores, regions_france


def plot_map(
    csv_file_path=None,
    str="not specified value",
    title="Default",
    range_color=None,
    points=None,
):
    """
    Plot a choropleth map based on the provided data.

    Parameters:
    - csv_file_path (str): Path to the CSV file containing the data. If None, dummy data will be used.
    - str (str): The column name in the CSV file to be used for coloring the map. Default is "not specified value".
    - title (str): The title of the map. Default is "Default".
    - range_color (list): The range of values to be used for coloring the map. If None, the range will be determined automatically.
    - points (list): List of coordinates (latitude, longitude) to be plotted as scatter points on the map. Default is None.

    Returns:
    None
    """

    if csv_file_path is None:
        # Dummy data for the regions of France
        values = np.random.rand(len(regions_france))  # Random values for demonstration
        values = values * 1000  # Scale the values between 0 and 1000

        # Create a DataFrame
        df = pd.DataFrame({"region_name": regions_france, str: values})

        str = "Dummy data"
    else:
        df = pd.read_csv(csv_file_path)

    if range_color is None and str != "Dummy data" and str != "not specified value":
        range_color = [df[str].min(), df[str].max()]
    else:
        if range_color is None:
            range_color = [0, 1000]

    # Create a choropleth map
    fig = px.choropleth(
        df,
        geojson="https://france-geojson.gregoiredavid.fr/repo/regions.geojson",
        featureidkey="properties.nom",
        locations="region_name",
        color=str,
        range_color=range_color,
        color_continuous_scale="gray_r",
        scope="europe",
        labels={"Value": str},
    )

    # Adjust the map to focus on France
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={
            "r": 100,
            "t": 100,
            "l": 100,
            "b": 100,
        },  # Adjust these values as needed to center the plot
    )

    # Add a border around the figure
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0.23,
                y0=0.01,
                x1=0.77,
                y1=0.99,
                line=dict(
                    color="Black",
                    width=3,
                ),
            )
        ]
    )

    fig.add_trace(
        go.Scattergeo(
            lon=df["lon"],
            lat=df["lat"],
            text=df[str],
            mode="text",
            textfont=dict(color="white", size=15, family="Arial, bold"),
            name="",
        )
    )

    if points is not None:
        # Add department coordinates as scatter points on the map

        # Create a DataFrame for all the stores
        df_stores = pd.DataFrame(points).T.reset_index()
        df_stores.columns = ["store_name", "lat", "lon"]

        fig.add_trace(
            go.Scattergeo(
                lon=df_stores["lon"],
                lat=df_stores["lat"],
                text=df_stores["store_name"],
                mode="markers",
                marker=dict(
                    size=10,
                    color="red",
                ),
                name="CORA stores not scraped",
            )
        )

        # Create a DataFrame for all the stores we scraped
        df_stores_scraped = pd.DataFrame(coords_scraped_stores).T.reset_index()
        df_stores_scraped.columns = ["store_name", "lat", "lon"]

        fig.add_trace(
            go.Scattergeo(
                lon=df_stores_scraped["lon"],
                lat=df_stores_scraped["lat"],
                text=df_stores_scraped["store_name"],
                mode="markers",
                marker=dict(
                    size=10,
                    color="blue",
                ),
                name="CORA stores scraped",
            )
        )

    # Add a legend
    fig.update_layout(
        showlegend=False,
        legend=dict(x=0.5, y=0.08, xanchor="center", yanchor="bottom"),
        title=dict(x=0.5, y=0.85, xanchor="center", yanchor="bottom"),
    )

    # Add a title
    fig.update_layout(title_text=title)

    # Show the figure
    fig.show()


if __name__ == "__main__":
    pass
