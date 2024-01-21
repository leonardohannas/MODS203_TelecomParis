import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go

regions = ["Île-de-France", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Occitanie", 
           "Hauts-de-France", "Grand Est", "Bretagne", "Normandie", "Pays de la Loire", 
           "Centre-Val de Loire", "Bourgogne-Franche-Comté", "Provence-Alpes-Côte d'Azur", 
           "Corse"]

stores_coords = {
    'Dijon': (47.2704586258, 5.0035427725),
    'Alès': (44.1126654809, 4.096759299),
    'Amphion': (46.3908762209, 6.5261565597),
    'Arcueil': (48.8052598743, 2.3255062427),
    'Auxerre': (47.8448500303, 3.5519833872),
    'Blois': (47.6221579711, 1.2962194206),
    'Bruay': (50.4949462713, 2.5719957359),
    'Clermont-Ferrand': (45.7790428005, 3.1974005835),
    'Caen': (49.1991833604, -0.4601216558),
    'Dorlisheim': (48.5269298025, 7.4966779354),
    'Dunkerque': (51.0163731709, 2.3802742805),
    'Ermont': (48.9884531968, 2.2467983228),
    "Flers-Villeneuve d'Ascq": (50.6361692024, 3.1202058386),
    'Garges': (48.9747335505, 2.416622396),
    'Limoges': (45.8797235605, 1.2920488444),
    'Massy': (48.7264243781, 2.2775803429),
    'Rennes': (48.1386869669, -1.7672960486),
    'Verdun': (49.1425255404, 5.4072061268)
}

def plot_map(csv_file_path=None, str="not specified value", range_color=None):

    if csv_file_path is None:
        # Dummy data for the regions of France
        values = np.random.rand(len(regions))  # Random values for demonstration
        values = values * 1000  # Scale the values between 0 and 1000

        # Create a DataFrame
        df = pd.DataFrame({
            'region_name': regions,
            str: values
        })

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
                        locations='region_name', 
                        color=str,
                        range_color = range_color,
                        color_continuous_scale= "gray_r",
                        scope="europe",
                        labels={'Value':str},
                        )

    # Adjust the map to focus on France
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 100, "t": 100, "l": 100, "b": 100},  # Adjust these values as needed to center the plot
    )

    # Add a border around the figure
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0.23, y0=0.01, x1=0.77, y1=0.99,
                line=dict(
                    color="Black",
                    width=3,
                ),
            )
        ]
    )

    # Add department coordinates as scatter points on the map

    # Create a DataFrame for departments
    df_stores = pd.DataFrame(stores_coords).T.reset_index()
    df_stores.columns = ['department_name', 'lat', 'lon']

    fig.add_trace(
        go.Scattergeo(
        lon = df_stores['lon'],
        lat = df_stores['lat'],
        text = df_stores['department_name'],
        mode = 'markers',
        marker = dict(
            size = 10,
            color = 'red',
        ),
        name="",
        )
    )

    # add a title
    fig.update_layout(title_text = str + ' by region in France')

    # Show the figure
    fig.show()

if __name__ == "__main__":

    # filepath = "data/filtered_magasin_product.csv"
    # df = pd.read_csv(filepath)

    # df_mean_n = df.groupby("region_name")["nutri_score_num"].mean()
    # df_mean_n = df_mean_n.reset_index()
    # df_mean_n = df_mean_n.sort_values(by="nutri_score_num", ascending=False)
    # df_mean_n.to_csv("data/mean_n_summary.csv")


    filepath = "data/min_zeros_summary.csv"
    plot_map(csv_file_path=filepath, str="zeros", range_color=[0, 1000])