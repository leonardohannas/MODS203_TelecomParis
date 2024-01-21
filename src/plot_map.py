import plotly.express as px
import pandas as pd
import numpy as np

def plot_map(csv_file_path=None, str="not specified value"):

    if csv_file_path is None:
        # Dummy data for the regions of France
        regions = ["Île-de-France", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Occitanie", 
           "Hauts-de-France", "Grand Est", "Bretagne", "Normandie", "Pays de la Loire", 
           "Centre-Val de Loire", "Bourgogne-Franche-Comté", "Provence-Alpes-Côte d'Azur", 
           "Corse"]

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
    
    # Create a choropleth map
    fig = px.choropleth(df, 
                        geojson="https://france-geojson.gregoiredavid.fr/repo/regions.geojson", 
                        featureidkey="properties.nom",
                        locations='region_name', 
                        color=str,
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

    # add a title
    fig.update_layout(title_text = str + ' by region in France')

    # Show the figure
    fig.show()

if __name__ == "__main__":
    filepath = "data/updated_summary.csv"
    plot_map(csv_file_path=filepath, str="min price [€]")