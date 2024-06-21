import geopandas as gpd
import pandas as pd
import os

# Define the paths
public_right_of_way_folder = 'sjshape/Public_Right_of_Way'
output_csv_path = 'out/public_right_of_way_data.csv'

# Function to extract and simplify data from Public Right of Way shapefiles
def extract_and_simplify_shapefiles(folder_path, output_csv_path, tolerance=0.01):
    shapefiles = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.shp')]
    data_frames = []
    
    for shapefile in shapefiles:
        gdf = gpd.read_file(shapefile)
        
        # Simplify geometries with higher tolerance
        gdf['geometry'] = gdf['geometry'].simplify(tolerance, preserve_topology=True)
        
        # Filter out unnecessary columns (example: keep only 'geometry')
        columns_to_keep = ['geometry']
        gdf = gdf[columns_to_keep]
        
        data_frames.append(gdf)
    
    # Concatenate all data frames into one
    combined_gdf = pd.concat(data_frames, ignore_index=True)
    
    # Save the combined data to a CSV file
    combined_gdf.to_csv(output_csv_path, index=False)

# Extract and simplify data from shapefiles and save to CSV
extract_and_simplify_shapefiles(public_right_of_way_folder, output_csv_path, tolerance=0.01)

print(f"Data extracted and saved to {output_csv_path}")
