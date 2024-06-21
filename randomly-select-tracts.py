import pandas as pd
import geopandas as gpd

# Define the paths
combined_csv_path = 'out/combined_data.csv'
sampled_csv_path = 'out/sampled_combined_data.csv'

# Load the combined CSV data
combined_data = pd.read_csv(combined_csv_path)

# Split the data into disadvantaged and non-disadvantaged
disadvantaged = combined_data[combined_data['Identified as disadvantaged'] == True]
non_disadvantaged = combined_data[combined_data['Identified as disadvantaged'] != True]

# Calculate the number of samples to take
n_total = int(len(combined_data) * 0.4)
n_disadvantaged = int(n_total * 0.4)
n_non_disadvantaged = n_total - n_disadvantaged

# Randomly sample from each group
sampled_disadvantaged = disadvantaged.sample(n=n_disadvantaged, random_state=1)
sampled_non_disadvantaged = non_disadvantaged.sample(n=n_non_disadvantaged, random_state=1)

# Combine the sampled data
sampled_combined_data = pd.concat([sampled_disadvantaged, sampled_non_disadvantaged])

# Save the sampled data to a CSV file
sampled_combined_data.to_csv(sampled_csv_path, index=False)

print(f"Sampled data saved to {sampled_csv_path}")
