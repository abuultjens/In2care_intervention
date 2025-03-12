import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# X-axis tick interval
X_AXIS_TICK_INTERVAL = 5

# line colours
CASES_LINE_COLOR = '#D55E00'
CASES_LINE_WIDTH = 3
EGG_LINE_COLOR = '#56B4E9'
EGG_LINE_WIDTH = 3
VERTICAL_LINE_COLOR = '#0072B2'
VERTICAL_LINE_WIDTH = 2

# marker
EGG_MARKER_SIZE = 100

# font sizes
TICK_FONT_SIZE = 20
AXIS_LABEL_FONT_SIZE = 20
PLOT_TITLE_FONT_SIZE = 20

# legend pos
LEGEND_X = -0.005
LEGEND_Y = 1.015

# legend text font size
LEGEND_TEXT_FONT_SIZE = 15

# updated data file
file_path = "FULL_impute_FET_CP_and_egg_count_NAs_egg-diff_v2.csv"
data = pd.read_csv(file_path)

# make numeric columns
columns_to_process = ['egg_counts_diff', 'treatment_mean_diff']
data[columns_to_process] = data[columns_to_process].apply(pd.to_numeric, errors='coerce')

# convert timestamp column to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%d.%m.%Y', errors='coerce')

# log the egg counts
data['egg_counts_diff_logged'] = np.log1p(data['egg_counts_diff'])  # log(x+1) to handle zeros safely

# get the non-NA egg count dates
egg_non_na_data = data.dropna(subset=['egg_counts_diff_logged'])

# get data for time-series plotting
time_series_data = data[['Timestamp', 'egg_counts_diff_logged', 'treatment_mean_diff']]

# highlight windows
highlight_windows = [
    "09.01.2024",
    "16.01.2024",
    "23.01.2024",
    "28.03.2024",
    "04.04.2024",
    "11.04.2024",
    "18.04.2024"
]

# get date format in highlight_windows exactly matches the Timestamp column
highlight_data = egg_non_na_data[egg_non_na_data['Timestamp'].dt.strftime('%d.%m.%Y').isin(highlight_windows)]

# plot the data
fig, ax1 = plt.subplots(figsize=(12, 5))

# plot the treatment mean difference
ax1.plot(
    time_series_data['Timestamp'],
    time_series_data['treatment_mean_diff'],
    label='Cases Prevented',
    color=CASES_LINE_COLOR,
    linewidth=CASES_LINE_WIDTH
)
ax1.set_ylabel("Cases prevented", color=CASES_LINE_COLOR, fontsize=AXIS_LABEL_FONT_SIZE)
ax1.tick_params(axis='y', labelcolor=CASES_LINE_COLOR, labelsize=TICK_FONT_SIZE)

# add a second y-axis for the egg counts
ax2 = ax1.twinx()

# plot egg counts
ax2.plot(
    egg_non_na_data['Timestamp'],
    egg_non_na_data['egg_counts_diff_logged'],
    linestyle=':',
    color=EGG_LINE_COLOR,
    linewidth=EGG_LINE_WIDTH,
    label='Imputed egg counts'
)

# add dot markers only for the specified windows
ax2.scatter(
    highlight_data['Timestamp'],
    highlight_data['egg_counts_diff_logged'],
    color=EGG_LINE_COLOR,
    marker='o',
    s=EGG_MARKER_SIZE,
    label='Actual egg counts'
)

ax2.set_ylabel("Egg count log difference", color=EGG_LINE_COLOR, fontsize=AXIS_LABEL_FONT_SIZE)
ax2.tick_params(axis='y', labelcolor=EGG_LINE_COLOR, labelsize=TICK_FONT_SIZE)

# add vertical dotted lines at the dates
important_dates = ["25.01.2024", "21.03.2024"]
important_dates = [datetime.strptime(date, "%d.%m.%Y") for date in important_dates]
for date in important_dates:
    ax1.axvline(date, color=VERTICAL_LINE_COLOR, linestyle='dashed', linewidth=VERTICAL_LINE_WIDTH)

# add a small horizontal margin
ax1.margins(x=0.05)

# format the x-axis labels correctly
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=X_AXIS_TICK_INTERVAL))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
plt.xticks(rotation=45, ha='right')

# format the plot
ax1.set_title("Egg Count Differences and Estimated Cases Prevented", fontsize=PLOT_TITLE_FONT_SIZE)

# combine legends from both axes and add the vertical line
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
vertical_line_legend = plt.Line2D([], [], color=VERTICAL_LINE_COLOR, linestyle='dashed', linewidth=VERTICAL_LINE_WIDTH, label='Start/end of intervention')
handles = lines_1 + lines_2 + [vertical_line_legend]
labels = labels_1 + labels_2 + ['Start/end of intervention']
ax1.legend(handles, labels, fontsize=LEGEND_TEXT_FONT_SIZE, loc='upper left', bbox_to_anchor=(LEGEND_X, LEGEND_Y))

ax1.grid(alpha=0.3)
plt.tight_layout()

# save the figure
plt.savefig('Fig3_C.svg', format='svg')
plt.savefig('Fig3_C.png', format='png')

plt.show()
