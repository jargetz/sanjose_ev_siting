import pandas as pd

# Define the path to the extracted CSV
public_right_of_way_csv_path = 'out/public_right_of_way_data.csv'

# Load the CSV data
public_right_of_way_data = pd.read_csv(public_right_of_way_csv_path)

# Print the first few rows to verify the data
print(public_right_of_way_data.head())
print(public_right_of_way_data.columns)
