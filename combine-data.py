import geopandas as gpd
import pandas as pd

# Define the paths
san_jose_shapefile_path = 'sjshape/san_jose_census_tracts.shp'
census_tract_csv_path = './Census_Tract.csv'
disadvantaged_csv_path = './filtered_santa_clara_data.csv'
combined_csv_path = 'out/combined_data.csv'

# Load the San Jose shapefile
gdf = gpd.read_file(san_jose_shapefile_path)

# Load the Census Tract CSV
census_tract_data = pd.read_csv(census_tract_csv_path)

# Load the Disadvantaged Data CSV
disadvantaged_data = pd.read_csv(disadvantaged_csv_path)

# Convert the GEOID10 and Census tract IDs to string for consistency
gdf['GEOID10'] = gdf['GEOID10'].astype(str)
census_tract_data['FIPSCODE'] = census_tract_data['FIPSCODE'].astype(str).str.zfill(len(gdf['GEOID10'].iloc[0]))
disadvantaged_data['Census tract 2010 ID'] = disadvantaged_data['Census tract 2010 ID'].astype(str).str.zfill(len(gdf['GEOID10'].iloc[0]))

# Filter the GeoDataFrame to include only San Jose tracts
san_jose_gdf = gdf[gdf['GEOID10'].isin(census_tract_data['FIPSCODE'])]

# Merge the filtered GeoDataFrame with the Disadvantaged Data
combined_gdf = san_jose_gdf.merge(disadvantaged_data, left_on='GEOID10', right_on='Census tract 2010 ID', how='left')

# Save the combined data to a CSV file
combined_gdf.to_csv(combined_csv_path, index=False)

print(f"Combined data saved to {combined_csv_path}")
