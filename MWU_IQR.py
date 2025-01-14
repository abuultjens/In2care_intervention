import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data files
data_file = 'Essendon_all_symptom_date.csv'
#data_file = 'Essendon_2022_sympthom.csv'
#treatment_sites_file = 'Control_lat_lon.csv'
treatment_sites_file = 'Treatment_lat_lon.csv'

# Read datasets
data = pd.read_csv(data_file)
treatment_sites = pd.read_csv(treatment_sites_file)

# Ensure 'unix_time' is properly recognized as a numerical column
data['unix_time'] = pd.to_numeric(data['unix_time'], errors='coerce')

# Define the UNIX time range for 30.05.2024 - 09.08.2024
start_date = datetime.strptime("30.05.2024", "%d.%m.%Y")
end_date = datetime.strptime("09.08.2024", "%d.%m.%Y")
start_unix = int(start_date.timestamp())
end_unix = int(end_date.timestamp())

# Add a column to classify the cases
data["class"] = np.where(
    (data["unix_time"] >= start_unix) & (data["unix_time"] <= end_unix),
    "Within_IQR",
    "Outside_IQR"
)

# Calculate proximity to the nearest treatment site
sample_coords = data[['lat', 'lon']].to_numpy()
site_coords = treatment_sites[['lat', 'lon']].to_numpy()
distances = np.sqrt(((sample_coords[:, None, :] - site_coords[None, :, :])**2).sum(axis=2)) * 111.32  # Convert to km
data['proximity_to_site'] = distances.min(axis=1)

# Split the data into the two groups
within_period = data[data['class'] == "Within_IQR"]['proximity_to_site']
outside_period = data[data['class'] == "Outside_IQR"]['proximity_to_site']

# Perform a Mann-Whitney U test to compare the two groups
u_stat, p_value = mannwhitneyu(within_period, outside_period, alternative='two-sided')

# Summary statistics
summary_stats = {
    "Within_IQR Mean Proximity (km)": within_period.mean(),
    "Outside_IQR Mean Proximity (km)": outside_period.mean(),
    "Mann-Whitney U Statistic": u_stat,
    "P-value": p_value
}

print("Summary Statistics:", summary_stats)

# Prepare data for plotting
plot_data = pd.DataFrame({
    "Proximity to Nearest Treatment Site (km)": pd.concat([within_period, outside_period]),
    "Class": ["Within_IQR"] * len(within_period) + ["Outside_IQR"] * len(outside_period)
})

# Plot the boxplot
plt.figure(figsize=(8, 6))
sns.boxplot(
    data=plot_data,
    x="Class",
    y="Proximity to Nearest Treatment Site (km)",
    palette={"Within_IQR": "red", "Outside_IQR": "green"}
)

# Add plot details
plt.title("Distance to treatment Sites [MWU=402.0, p-value=0.714]", fontsize=16)
plt.xlabel("Class", fontsize=14)
plt.ylabel("Distance to nearest treatment site (kilometers)", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()
