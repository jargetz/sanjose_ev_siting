import pandas as pd
import geopandas as gpd
import folium
import zipfile
import os
from shapely.geometry import box

# Define the paths
zip_file_path = './usa.zip'
extraction_path = 'extraction'
output_shapefile_path = './san_jose_census_tracts.shp'

# Create the extraction directory if it doesn't exist
os.makedirs(extraction_path, exist_ok=True)

# Extract the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_path)

# Load the shapefile from the extracted files
shapefile_path = os.path.join(extraction_path, 'usa.shp')
gdf = gpd.read_file(shapefile_path)

# Define the bounding box for San Jose (approximate coordinates)
minx, miny, maxx, maxy = -122.045, 37.200, -121.550, 37.469

# Create a bounding box
bbox = box(minx, miny, maxx, maxy)

# Filter the GeoDataFrame for census tracts within the bounding box
filtered_gdf = gdf[gdf.intersects(bbox)]

# Save the filtered GeoDataFrame to a new shapefile
filtered_gdf.to_file(output_shapefile_path, driver='ESRI Shapefile')

# Create a base map centered on San Jose
m = folium.Map(location=[37.3382, -121.8863], zoom_start=12)

# Add the census tracts to the map
folium.GeoJson(filtered_gdf).add_to(m)

# Save the map to an HTML file
map_file_path = 'san_jose_census_tracts_map.html'
m.save(map_file_path)

print(f"Filtered shapefile saved to {output_shapefile_path}")
print(f"Map saved to {map_file_path}")
