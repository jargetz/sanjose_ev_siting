import geopandas as gpd
import os

# Define the folder path
shapefiles_folder = 'sjshape/Public_Right_of_Way'

# Get a list of all shapefiles in the folder
shapefiles = [os.path.join(shapefiles_folder, f) for f in os.listdir(shapefiles_folder) if f.endswith('.shp')]

# Function to check for census tract data
def check_for_census_tract_data(shapefile):
    gdf = gpd.read_file(shapefile)
    print(f"Checking {shapefile}")
    print("Columns:", gdf.columns)
    if 'GEOID10' in gdf.columns or 'Census tract' in gdf.columns or 'FIPSCODE' in gdf.columns:
        print("Census tract data found in this shapefile.")
    else:
        print("No census tract data found in this shapefile.")
    print("\n")

# Iterate over each shapefile and check for census tract data
for shapefile in shapefiles:
    check_for_census_tract_data(shapefile)
