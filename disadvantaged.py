import pandas as pd
import geopandas as gpd
import folium
from shapely import wkt
from shapely.geometry import Point
import base64
import requests
import numpy as np

# Define the paths
combined_csv_path = 'out/combined_data.csv'
traffic_data_path = './data/Average_Daily_Traffic.csv'
output_map_path = 'out/pages/combined_data_map_with_traffic.html'
output_map_path_index = './index.html'
statistics_output_path = 'out/statistics.csv'
outliers_output_path = 'out/outliers.csv'
icon_path = './electric-vehicle-charging-station-icon.png'
api_key_path = './.ocm.key'

# Load the OpenChargeMap API key
with open(api_key_path, 'r') as file:
    api_key = file.read().strip()

# Load the combined CSV data
combined_data = pd.read_csv(combined_csv_path)

# Convert the 'geometry' column to actual geometry objects
combined_data['geometry'] = combined_data['geometry'].apply(wkt.loads)
combined_gdf = gpd.GeoDataFrame(combined_data, geometry='geometry')

# Set the CRS for the combined GeoDataFrame
combined_gdf.set_crs(epsg=4326, inplace=True)

# Load the traffic data
traffic_data = pd.read_csv(traffic_data_path)

# Convert traffic data to GeoDataFrame
traffic_data['geometry'] = traffic_data.apply(lambda row: Point(row['LONGITUDE'], row['LATITUDE']), axis=1)
traffic_gdf = gpd.GeoDataFrame(traffic_data, geometry='geometry')

# Set the CRS for the traffic GeoDataFrame to match the census tracts
traffic_gdf.set_crs(epsg=4326, inplace=True)

# Calculate mean and standard deviation for 'ADT'
mean_adt = traffic_gdf['ADT'].mean()
std_adt = traffic_gdf['ADT'].std()

# Filter traffic data points to only include those greater than the mean plus one standard deviation
filtered_traffic_gdf = traffic_gdf[traffic_gdf['ADT'] > mean_adt + std_adt]

# Spatial join to assign traffic data points to census tracts
joined_gdf = gpd.sjoin(filtered_traffic_gdf, combined_gdf, how='left', op='within')

# Save the joined data to CSV
joined_gdf.to_csv('out/joined_traffic_data.csv', index=False)

# Calculate mean and standard deviation for 'Diesel particulate matter exposure'
mean_exposure = combined_gdf['Diesel particulate matter exposure'].mean()
std_exposure = combined_gdf['Diesel particulate matter exposure'].std()

# Export statistics to CSV
statistics = pd.DataFrame({
    'Metric': ['Mean', 'Standard Deviation'],
    'ADT': [mean_adt, std_adt],
    'Diesel particulate matter exposure': [mean_exposure, std_exposure]
})
statistics.to_csv(statistics_output_path, index=False)

# Identify outliers in both ADT and diesel particulate matter exposure
outliers_gdf = combined_gdf[
    (combined_gdf['Diesel particulate matter exposure'] > mean_exposure + std_exposure) & 
    (combined_gdf['GEOID10'].isin(joined_gdf['GEOID10']))
]

# Save the outliers to CSV with specified columns only
outliers_gdf[['GEOID10', 'SF', 'CF', 'Diesel particulate matter exposure']].to_csv(outliers_output_path, index=False)

# Create a base map centered on San Jose
m = folium.Map(location=[37.3382, -121.8863], zoom_start=12)

# Define the style function for census tracts
def style_function(feature):
    props = feature['properties']
    exposure = props.get('Diesel particulate matter exposure', 0)
    if (exposure > mean_exposure + std_exposure) and props.get('Identified as disadvantaged', False):
        return {
            'fillColor': 'red',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.2,  # 80% transparent red
        }
    elif props.get('Identified as disadvantaged', False):
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

# Define the style function for outliers
def outlier_style_function(feature):
    return {
        'fillColor': 'red',
        'color': 'darkblue',
        'weight': 1,  # 1px thick dark blue border
        'fillOpacity': 0.2,  # 80% transparent red
    }

# Add the census tracts to the map
folium.GeoJson(
    combined_gdf,
    style_function=style_function
).add_to(m)

# Add the outliers to the map with a thicker border
folium.GeoJson(
    outliers_gdf,
    style_function=outlier_style_function
).add_to(m)

# Calculate the centroid of each sampled tract to place the pin
sampled_combined_data = combined_gdf.sample(n=50, random_state=1)  # Adjust sampling as needed
sampled_combined_data['centroid'] = sampled_combined_data.geometry.centroid

# Encode the icon to base64
with open(icon_path, 'rb') as image_file:
    encoded_icon = base64.b64encode(image_file.read()).decode()

# Add a pin to the centroid of each selected tract with custom icon
icon_url = f"data:image/png;base64,{encoded_icon}"
icon_size = (15, 15)  # 50% smaller than typical size (30, 30)

for idx, row in sampled_combined_data.iterrows():
    centroid = row['centroid']
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Census Tract: {row['GEOID10']}",
        icon=folium.CustomIcon(icon_url, icon_size=icon_size)
    ).add_to(m)

# Fetch EV charger data from OpenChargeMap API
params = {
    'output': 'json',
    'latitude': 37.3382,
    'longitude': -121.8863,
    'distance': 10,  # Radius in miles
    'maxresults': 100,
    'key': api_key,
    'minpowerkw': 50,
    'status_type': 'Operational',
    'access_type': 'Public'
}
response = requests.get('https://api.openchargemap.io/v3/poi', params=params)

# Check if the request was successful
if response.status_code == 200:
    ev_chargers_data = response.json()
    # Add EV charger locations to the map
    for station in ev_chargers_data:
        location = station['AddressInfo']
        folium.Marker(
            location=[location['Latitude'], location['Longitude']],
            popup=f"EV Charger: {location['Title']}",
            icon=folium.Icon(color='green', icon='flash', prefix='fa')
        ).add_to(m)
else:
    print("Failed to fetch EV charger data")

# Add filtered traffic data points to the map
for idx, row in filtered_traffic_gdf.iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=3,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"Traffic Data Point: LAT={row['LATITUDE']}, LON={row['LONGITUDE']}, ADT={row['ADT']}"
    ).add_to(m)

# Save the map to an HTML file
m.save(output_map_path)
m.save(output_map_path_index)

print(f"Map saved to {output_map_path}")
print(f"Statistics saved to {statistics_output_path}")
print(f"Outliers saved to {outliers_output_path}")
