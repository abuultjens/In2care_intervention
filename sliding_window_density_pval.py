import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore

# Load the updated CSV file
file_path = '2024_control_sliding_window_mean-diff_rand-coords_report_ACTUAL_AND_RAND-1-9.csv'
data = pd.read_csv(file_path)

# Separate the columns
timestamps = data.iloc[:, 0]  # First column as x-axis labels (strings)
actual_treatment_data = data.iloc[:, 1]  # Second column as actual treatment data
actual_control_data = data.iloc[:, 2]  # Third column as actual control data
random_data = data.iloc[:, 3:]  # Columns to the right as random data

# Extract the start date from the date range (e.g., "13.4.2024-23.6.2024" -> "13.4.2024")
def extract_start_date(date_range):
    try:
        return pd.to_datetime(date_range.split('-')[0].strip(), format='%d.%m.%Y', errors='coerce')
    except Exception:
        return None

# Apply extraction and clean dates
start_dates = timestamps.apply(extract_start_date)
valid_mask = start_dates.notna()  # Mask for valid start dates
start_dates = start_dates[valid_mask]
actual_treatment_data = actual_treatment_data[valid_mask]
actual_control_data = actual_control_data[valid_mask]
random_data = random_data[valid_mask]

# Filter data from "13.4.2024" onwards
mask = start_dates >= pd.Timestamp('2024-04-13')
start_dates = start_dates[mask]
timestamps = timestamps[mask]  # Retain the original range strings for x-axis labels
actual_treatment_data = actual_treatment_data[mask]
actual_control_data = actual_control_data[mask]
random_data = random_data[mask]

# Calculate p-value thresholds (5th and 95th percentiles of random data for each time point)
lower_p_threshold = random_data.quantile(0.05, axis=1).values  # 5th percentile
upper_p_threshold = random_data.quantile(0.95, axis=1).values  # 95th percentile

# Plotting
plt.figure(figsize=(12, 8))

# Highlight the region where p-values are greater than 0.05
plt.fill_between(
    range(len(timestamps)), lower_p_threshold, upper_p_threshold, color='gray', alpha=0.2, label='p-value > 0.05 region'
)

# Plot the actual treatment and control data
plt.plot(range(len(timestamps)), actual_treatment_data, color='red', linewidth=2, label='Actual treatment sites')
plt.plot(range(len(timestamps)), actual_control_data, color='green', linewidth=2, label='Actual control sites')

# Add plot details
plt.title(
    'Difference in mean distance to nearest treatment site:\n'
    '71-day sliding windows with actual vs randomized treatment coordinates',
    fontsize=16
)
plt.xlabel('71 day window start and stop dates', fontsize=14)
plt.ylabel('Mean difference in distance to nearest treatment site', fontsize=14)

# Use every third x-axis label
plt.xticks(
    ticks=range(0, len(timestamps), 3),  # Every third label
    labels=timestamps.iloc[::3],  # Keep the original range strings for the x-axis
    rotation=90, 
    fontsize=8
)

# Set the legend in the top-left corner
plt.legend(fontsize=12, loc='upper left')
plt.tight_layout()

# Show the plot
plt.show()
