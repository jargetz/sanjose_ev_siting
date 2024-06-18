import pandas as pd
import geopandas as gpd
import folium
import os

# Define the paths
san_jose_shapefile_path = 'sjshape/san_jose_census_tracts.shp'
csv_file_path = './filtered_santa_clara_data.csv'
san_jose_csv_path = './Census_Tract.csv'
output_map_path = 'out/san_jose_census_tracts_map.html'
public_right_of_way_folder = 'sjshape/Public_Right_of_Way'

# Load the San Jose shapefile
gdf = gpd.read_file(san_jose_shapefile_path)

# Load the CSV data
data = pd.read_csv(csv_file_path)

# Load the San Jose census tracts CSV
sj_data = pd.read_csv(san_jose_csv_path)

# Convert the columns to strings to ensure they have the same data type
gdf['GEOID10'] = gdf['GEOID10'].astype(str)
data['Census tract 2010 ID'] = data['Census tract 2010 ID'].astype(str).str.zfill(len(gdf['GEOID10'].iloc[0]))
sj_data['FIPSCODE'] = sj_data['FIPSCODE'].astype(str).str.zfill(len(gdf['GEOID10'].iloc[0]))

# Filter the GeoDataFrame to include only San Jose tracts
san_jose_gdf = gdf[gdf['GEOID10'].isin(sj_data['FIPSCODE'])]

# Merge the filtered GeoDataFrame with the CSV data based on the census tract key
merged_gdf = san_jose_gdf.merge(data, left_on='GEOID10', right_on='Census tract 2010 ID', how='left')

# Create a base map centered on San Jose
m = folium.Map(location=[37.3382, -121.8863], zoom_start=12)

# Define the style function for census tracts
def style_function(feature):
    if 'Identified as disadvantaged' in feature['properties'] and feature['properties']['Identified as disadvantaged']:
        return {
            'fillColor': 'purple',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.35,  # 30% more transparent purple
        }
    else:
        return {
            'fillColor': 'yellow',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.1,  # 90% transparent yellow
        }

# Add the census tracts to the map
folium.GeoJson(
    merged_gdf,
    style_function=style_function
).add_to(m)

# Function to add Public Right of Way shapefiles to the map
def add_public_right_of_way(m, folder_path):
    shapefiles = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.shp')]
    for shapefile in shapefiles:
        gdf = gpd.read_file(shapefile)
        folium.GeoJson(gdf, style_function=lambda x: {
            'color': 'blue',
            'weight': 2,
            'fillOpacity': 0
        }).add_to(m)

# Add Public Right of Way shapefiles to the map
add_public_right_of_way(m, public_right_of_way_folder)

# Save the map to an HTML file
m.save(output_map_path)

print(f"Map saved to {output_map_path}")
