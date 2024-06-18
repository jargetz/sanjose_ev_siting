import geopandas as gpd

# Define the path to the San Jose shapefile
san_jose_shapefile_path = 'sjshape/san_jose_census_tracts.shp'

# Load the San Jose shapefile
gdf = gpd.read_file(san_jose_shapefile_path)

# Display the first few rows and the columns of the GeoDataFrame
print(gdf.head())
print(gdf.columns)
