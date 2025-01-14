import pandas as pd
from scipy.stats import percentileofscore

# Load the updated CSV file
file_path = '2024_control_sliding_window_mean-diff_rand-coords_report_ACTUAL_AND_RAND-1-9.csv'
data = pd.read_csv(file_path)

# Separate the columns
timestamps = data.iloc[:, 0]  # First column as x-axis labels (strings)
actual_treatment_data = data.iloc[:, 1]  # Second column as actual treatment data
actual_control_data = data.iloc[:, 2]  # Third column as actual control data
random_data = data.iloc[:, 3:]  # Columns to the right as random data

# Calculate p-values for the actual treatment and control data
treatment_p_values = [
    1 - (percentileofscore(random_data.iloc[i, :], actual_treatment_data.iloc[i]) / 100)
    for i in range(len(actual_treatment_data))
]

control_p_values = [
    1 - (percentileofscore(random_data.iloc[i, :], actual_control_data.iloc[i]) / 100)
    for i in range(len(actual_control_data))
]

# Create a DataFrame to store the results
report = pd.DataFrame({
    "Timestamp": timestamps,
    "Treatment P-value": treatment_p_values,
    "Control P-value": control_p_values
})

# Save the report to a CSV file
report_file_path = 'sliding_window_p_values_report.csv'
report.to_csv(report_file_path, index=False)

print(f"P-values report has been written to {report_file_path}.")
