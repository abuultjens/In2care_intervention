import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def main(data_file, treatment_sites_file, start_unix, end_unix):
    # Read datasets
    data = pd.read_csv(data_file)
    treatment_sites = pd.read_csv(treatment_sites_file)

    # Ensure 'unix_time' is properly recognized as a numerical column
    data['unix_time'] = pd.to_numeric(data['unix_time'], errors='coerce')

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

    # Calculate mean proximity for each class
    mean_within = within_period.mean()
    mean_outside = outside_period.mean()
    mean_difference = mean_within - mean_outside

    # Summary statistics
    summary_stats = {
        "Within_IQR Mean Proximity (km)": mean_within,
        "Outside_IQR Mean Proximity (km)": mean_outside,
        "Mean Difference (km)": mean_difference,
        "Mann-Whitney U Statistic": u_stat,
        "P-value": p_value
    }

    print("Summary Statistics:")
    for key, value in summary_stats.items():
        print(f"{key}: {value}")

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
    plt.title(f"Distance to treatment Sites [MWU={u_stat:.1f}, p-value={p_value:.3f}]", fontsize=16)
    plt.xlabel("Class", fontsize=14)
    plt.ylabel("Distance to nearest treatment site (kilometers)", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Show the plot
    plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    # Expecting positional arguments: data_file, treatment_sites_file, start_unix, end_unix
    if len(sys.argv) != 5:
        print("Usage: python script.py <data_file> <treatment_sites_file> <start_unix> <end_unix>")
        sys.exit(1)
    
    # Parse positional arguments
    data_file = sys.argv[1]
    treatment_sites_file = sys.argv[2]
    start_unix = int(sys.argv[3])
    end_unix = int(sys.argv[4])

    main(data_file, treatment_sites_file, start_unix, end_unix)
