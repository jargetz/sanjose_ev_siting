import pandas as pd
import matplotlib.pyplot as plt

# Load the data
combined_csv_path = './data/filtered_santa_clara_data.csv'
traffic_data_path = './data/Average_Daily_Traffic.csv'

combined_data = pd.read_csv(combined_csv_path)
traffic_data = pd.read_csv(traffic_data_path)

# Plot the distribution of 'Diesel particulate matter exposure' and 'ADT'
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Plot for Diesel particulate matter exposure
axes[0].hist(combined_data['Diesel particulate matter exposure'].dropna(), bins=50, color='purple', alpha=0.7)
axes[0].set_title('Distribution of Diesel Particulate Matter Exposure')
axes[0].set_xlabel('Diesel Particulate Matter Exposure')
axes[0].set_ylabel('Frequency')

# Plot for ADT
axes[1].hist(traffic_data['ADT'].dropna(), bins=50, color='blue', alpha=0.7)
axes[1].set_title('Distribution of Average Daily Traffic (ADT)')
axes[1].set_xlabel('Average Daily Traffic (ADT)')
axes[1].set_ylabel('Frequency')

plt.tight_layout()

# Save the plot
plot_path = './out/distribution_plot.png'
plt.savefig(plot_path)

print(f"Plot saved to {plot_path}")
