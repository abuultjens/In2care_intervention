import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta

# X-axis tick interval
X_AXIS_TICK_INTERVAL = 5

# lines for actual p-values
ACTUAL_2024_COLOR = '#D55E00' # Vermilion
ACTUAL_2024_WIDTH = 3
ACTUAL_2023_COLOR = '#56B4E9' # Sky Blue
ACTUAL_2023_WIDTH = 3

# lines for median of random data
MEDIAN_RANDOM_COLOR = '#000000'
MEDIAN_RANDOM_WIDTH = 3

# horizontal lines
PVALUE_THRESHOLD_COLOR = '#000000'
PVALUE_THRESHOLD_WIDTH = 1.5
BH_THRESHOLD_COLOR = '#000000'
BH_THRESHOLD_WIDTH = 1.5

# egg count data
EGG_COUNT_COLOR = '#CC79A7'
EGG_COUNT_WIDTH = 3

# transparency of legend box
LEGEND_ALPHA = 0.7

# legend font size
LEGEND_FONT_SIZE = 15 
LEGEND_COLUMN_SPACING = 0.5

# Y-axis limits
Y_AXIS_MIN = -0.1
Y_AXIS_MAX = 2.5

# secondary Y-axis limits
SECONDARY_Y_AXIS_MIN = 0
SECONDARY_Y_AXIS_MAX = 3.5 

# legend  coordinates
LEGEND_X = 0.0925
LEGEND_Y = 0.94

# axis tick font sizes
X_AXIS_TICK_FONT_SIZE = 14
Y_AXIS_TICK_FONT_SIZE = 20

# axis heading font size
AXES_HEADING_SIZE = 20

# x and y axis label font size
X_AXIS_LABEL_FONT_SIZE = 20
Y_AXIS_LABEL_FONT_SIZE = 20

# colour of the two vertical lines
VERTICAL_INTERVENTION_COLOR = '#0072B2' # Blue

# load the CSV file
file_path = '4.5-DATE_ESSENDON-AIRPORT_RAINFALL_2023-48_AND_2024-70_sliding_window_Haversine_zone-800m_FET_v1-PVAL_rand-coords_report_ACTUAL_AND_RAND.csv'
data = pd.read_csv(file_path, header=None)

# define column names
data.columns = ['Date', '2024_actual_p-values', '2023_actual_p-values', 'Egg_counts'] + \
               [f'Random_{i}' for i in range(1, data.shape[1] - 4 + 1)]

# convert Date column to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y', errors='coerce')

# filter out invalid dates
data = data.dropna(subset=['Date'])

# ensure data is sorted by date
data = data.sort_values(by='Date')

# extract the columns
actual_treatment_data = data['2024_actual_p-values']
actual_control_data = data['2023_actual_p-values']
egg_counts = data['Egg_counts']
random_data = data.iloc[:, 4:]

# fix divide-by-zero in log 
actual_treatment_data.replace(0, np.nan, inplace=True)
actual_control_data.replace(0, np.nan, inplace=True)
random_data.replace(0, np.nan, inplace=True)

# apply -log10 to p-values
actual_treatment_data = -np.log10(actual_treatment_data)
actual_control_data = -np.log10(actual_control_data)
random_data = -np.log10(random_data)

# number of tests
alpha = 0.05
num_tests = len(data)

# B-H corrected p-value threshold
p_values = 10 ** -actual_treatment_data.sort_values().values
bh_thresholds = (np.arange(1, num_tests + 1) / num_tests) * alpha
bh_p_value = max([p for p, t in zip(p_values, bh_thresholds) if p <= t], default=0)
bh_threshold = -np.log10(bh_p_value) if bh_p_value > 0 else Y_AXIS_MAX

# calculate percentiles for random data
lower_p_threshold = random_data.quantile(0.05, axis=1).values  # 5th percentile
upper_p_threshold = random_data.quantile(0.95, axis=1).values  # 95th percentile
lower_iqr = random_data.quantile(0.25, axis=1).values  # 25th percentile (IQR lower bound)
upper_iqr = random_data.quantile(0.75, axis=1).values  # 75th percentile (IQR upper bound)
median_random = random_data.quantile(0.5, axis=1).values  # Median of random data

# plotting
fig, ax1 = plt.subplots(figsize=(12, 6))

# plot p-value related data on primary y-axis
ax1.plot(data['Date'], actual_control_data, color=ACTUAL_2023_COLOR, linewidth=ACTUAL_2023_WIDTH, label='2023 cases')
ax1.plot(data['Date'], actual_treatment_data, color=ACTUAL_2024_COLOR, linewidth=ACTUAL_2024_WIDTH, label='2024 cases')
ax1.axhline(y=bh_threshold, color=BH_THRESHOLD_COLOR, linestyle='dashed', linewidth=BH_THRESHOLD_WIDTH, label='BH corrected threshold')
#ax1.plot(data['Date'], median_random, color=MEDIAN_RANDOM_COLOR, linestyle='-', linewidth=MEDIAN_RANDOM_WIDTH, label='Median of random data')
#ax1.fill_between(data['Date'], lower_iqr, upper_iqr, color='gray', alpha=0.4, label='IQR (25%-75%)')
#ax1.fill_between(data['Date'], lower_p_threshold, upper_p_threshold, color='gray', alpha=0.2, label='95th percentile of random')

# add vertical dashed lines with legend
for idx, date in enumerate(['25.01.2024', '21.03.2024']):
    ax1.axvline(pd.to_datetime(date, format='%d.%m.%Y'), color=VERTICAL_INTERVENTION_COLOR, linestyle='--', linewidth=2, 
                label='Start/end of intervention' if idx == 0 else '_nolegend_')

# add secondary y-axis for Egg_counts
#ax2 = ax1.twinx()
#ax2.plot(data['Date'], egg_counts, color=EGG_COUNT_COLOR, linewidth=EGG_COUNT_WIDTH, label='Rainfall (70 day rolling mean)')
#ax2.set_ylabel('Regional rainfall (mm/day)', fontsize=Y_AXIS_LABEL_FONT_SIZE, color=EGG_COUNT_COLOR)
#ax2.tick_params(axis='y', labelsize=Y_AXIS_TICK_FONT_SIZE, colors=EGG_COUNT_COLOR)

# set custom y-axis limits
ax1.set_ylim(Y_AXIS_MIN, Y_AXIS_MAX)
#ax2.set_ylim(SECONDARY_Y_AXIS_MIN, SECONDARY_Y_AXIS_MAX)

# add plot details
ax1.set_title('Fisher’s exact test p‑value distributions', fontsize=AXES_HEADING_SIZE)
ax1.set_xlabel('Exposure date (window contains cases with Sx onset 101-171 days later)', fontsize=X_AXIS_LABEL_FONT_SIZE)
ax1.set_ylabel("Fisher's exact -log(p-value)", fontsize=Y_AXIS_LABEL_FONT_SIZE)

# adjust x-axis to show more tick marks
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=X_AXIS_TICK_INTERVAL))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
fig.autofmt_xdate()

# adjust tick font size
ax1.tick_params(axis='x', labelsize=X_AXIS_TICK_FONT_SIZE)
ax1.tick_params(axis='y', labelsize=Y_AXIS_TICK_FONT_SIZE)

# set legend
fig.legend(loc='upper left', bbox_to_anchor=(LEGEND_X, LEGEND_Y), framealpha=LEGEND_ALPHA, fontsize=LEGEND_FONT_SIZE, ncol=1, columnspacing=LEGEND_COLUMN_SPACING)

# add faint vertical and horizontal grid lines
ax1.grid(alpha=0.3)

plt.tight_layout()

# save the figure
plt.savefig('Fig3_B_v2.svg', format='svg')
plt.savefig('Fig3_B_v2.png', format='png')

plt.show()
