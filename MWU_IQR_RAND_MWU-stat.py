import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data files
data_file = 'Essendon_all_symptom_date.csv'
treatment_sites_file = 'Control_lat_lon.csv'

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

# Function to calculate proximity to the nearest treatment site
def calculate_proximity(data, treatment_sites):
    sample_coords = data[['lat', 'lon']].to_numpy()
    site_coords = treatment_sites[['lat', 'lon']].to_numpy()
    distances = np.sqrt(((sample_coords[:, None, :] - site_coords[None, :, :])**2).sum(axis=2)) * 111.32  # Convert to km
    return distances.min(axis=1)

# Add proximity to the dataset
data['proximity_to_site'] = calculate_proximity(data, treatment_sites)

# Perform the analysis with actual data
data["class"] = np.where(
    (data["unix_time"] >= start_unix) & (data["unix_time"] <= end_unix),
    "Within Period",
    "Outside Period"
)
within_period = data[data['class'] == "Within Period"]['proximity_to_site']
outside_period = data[data['class'] == "Outside Period"]['proximity_to_site']
actual_stat, actual_p_value = mannwhitneyu(within_period, outside_period, alternative='two-sided')

# Run 100 randomizations
random_stats = []
np.random.seed(42)  # Set seed for reproducibility
for _ in range(1000):
    data['unix_time'] = np.random.permutation(data['unix_time'].values)
    data["class"] = np.where(
        (data["unix_time"] >= start_unix) & (data["unix_time"] <= end_unix),
        "Within Period",
        "Outside Period"
    )
    within_period = data[data['class'] == "Within Period"]['proximity_to_site']
    outside_period = data[data['class'] == "Outside Period"]['proximity_to_site']
    if len(within_period) > 0 and len(outside_period) > 0:
        stat, _ = mannwhitneyu(within_period, outside_period, alternative='two-sided')
        random_stats.append(stat)

# Plot the results
plt.figure(figsize=(10, 6))
sns.histplot(random_stats, kde=False, color="lightblue", bins=20, label="Runs with symptom date randomly reshuffled (n=1,000)")
plt.axvline(actual_stat, color="red", linestyle="--", label="Statistic from actual data")
plt.title("Distribution of Mann-Whitney U test statistic (randomised vs actual)", fontsize=16)
plt.xlabel("Mann-Whitney U statistic", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

# Print actual results
print(f"Actual Mann-Whitney U Statistic: {actual_stat}")
print(f"Actual P-value: {actual_p_value}")
