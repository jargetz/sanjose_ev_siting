import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Load the data
combined_csv_path = './data/filtered_santa_clara_data.csv'
traffic_data_path = './data/Average_Daily_Traffic.csv'

combined_data = pd.read_csv(combined_csv_path)
traffic_data = pd.read_csv(traffic_data_path)

# Normalize the data using z-score
combined_data['Diesel particulate matter exposure (z-score)'] = zscore(combined_data['Diesel particulate matter exposure'].dropna())
traffic_data['ADT (z-score)'] = zscore(traffic_data['ADT'].dropna())

# Plot the distribution of normalized 'Diesel particulate matter exposure' and 'ADT'
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Plot for normalized Diesel particulate matter exposure
axes[0].hist(combined_data['Diesel particulate matter exposure (z-score)'].dropna(), bins=50, color='purple', alpha=0.7)
axes[0].set_title('Normalized Distribution of Diesel Particulate Matter Exposure')
axes[0].set_xlabel('Diesel Particulate Matter Exposure (z-score)')
axes[0].set_ylabel('Frequency')

# Plot for normalized ADT
axes[1].hist(traffic_data['ADT (z-score)'].dropna(), bins=50, color='blue', alpha=0.7)
axes[1].set_title('Normalized Distribution of Average Daily Traffic (ADT)')
axes[1].set_xlabel('Average Daily Traffic (ADT) (z-score)')
axes[1].set_ylabel('Frequency')

plt.tight_layout()

# Save the plot
plot_path = './out/normalized_distribution_plot.png'
plt.savefig(plot_path)

print(f"Plot saved to {plot_path}")
