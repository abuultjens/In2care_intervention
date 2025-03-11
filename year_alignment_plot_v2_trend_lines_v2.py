import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta

# text sizes
# X-axis tick label text size
xtick_fontsize = 14 
# Y-axis tick label text size
ytick_fontsize = 14 
# X-axis label text size
xlabel_fontsize = 16 
# Y-axis label text size
ylabel_fontsize = 16 
# Title text size
title_fontsize = 18      
# Legend text size   
legend_fontsize = 14        

# trendline thickness
trendline_linewidth = 4

# olours for the bar plots
year_colors = {
    '2022': '#7fc97f', 
    '2023': '#386cb0',
    '2024': '#f0027f'
}
# colours for the trendlines
trendline_colors = {
    '2022': '#7fc97f',
    '2023': '#386cb0',
    '2024': '#f0027f'
}

# box and vertical line colours
intervention_box_color = '#beaed4'   # intervention period box
IQR_box_color = '#fdc086'           # IQR box
vertical_line_color = 'black'         # vertical line on 20/02/2024

# legend placement (x, y coordinates)
legend_loc_x = 0.65
legend_loc_y = 0.71
legend_loc = (legend_loc_x, legend_loc_y)

# load data files
data_file = 'Essendon_all_symptom_date.csv'
data_2023_file = 'Essendon_2023_sympthom.csv'
data_2022_file = 'Essendon_2022_sympthom.csv'

# read datasets
data = pd.read_csv(data_file)
data_2023 = pd.read_csv(data_2023_file)
data_2022 = pd.read_csv(data_2022_file)

# make sure unix_time is a numerical column
data['unix_time'] = pd.to_numeric(data['unix_time'], errors='coerce')
data_2023['unix_time'] = pd.to_numeric(data_2023['unix_time'], errors='coerce')
data_2022['unix_time'] = pd.to_numeric(data_2022['unix_time'], errors='coerce')

# convert UNIX time to datetime
data['datetime'] = pd.to_datetime(data['unix_time'], unit='s')
data_2023['datetime'] = pd.to_datetime(data_2023['unix_time'], unit='s')
data_2022['datetime'] = pd.to_datetime(data_2022['unix_time'], unit='s')

# add week column to align by week
data['week'] = data['datetime'].dt.isocalendar().week
data_2023['week'] = data_2023['datetime'].dt.isocalendar().week
data_2022['week'] = data_2022['datetime'].dt.isocalendar().week

# group cases by week for all years
cases_2024_weekly = data.groupby('week').size()
cases_2023_weekly = data_2023.groupby('week').size()
cases_2022_weekly = data_2022.groupby('week').size()

# combine aligned datasets by week
cases_weekly_aligned = pd.DataFrame({
    '2022': cases_2022_weekly,
    '2023': cases_2023_weekly,
    '2024': cases_2024_weekly
}).fillna(0)  # fill missing values with 0

# make bar plot using the year colours
ax = cases_weekly_aligned.plot(kind='bar', figsize=(14, 8),
                               color=[year_colors['2022'], year_colors['2023'], year_colors['2024']],
                               edgecolor='black', width=0.8)

# add smoothed trend lines
for year in cases_weekly_aligned.columns:
    smoothed = gaussian_filter1d(cases_weekly_aligned[year], sigma=2)  # Adjust sigma for smoothness
    ax.plot(smoothed, color=trendline_colors[year], label='_nolegend_', linewidth=trendline_linewidth)

# find the start date of each week for x-axis labels
week_starts = [
    pd.Timestamp('2024-01-25') + pd.Timedelta(weeks=week - 1)
    for week in cases_weekly_aligned.index
]
ax.set_xticks(range(len(week_starts)))  # Set ticks for all weeks
ax.set_xticklabels([date.strftime('%d/%m') for date in week_starts], rotation=90, ha='right')

# highlight intervention period (from 25.01.2024 to 21.03.2024)
intervention_start_date = pd.Timestamp('2024-01-25')
intervention_end_date = pd.Timestamp('2024-03-21')
intervention_start_pos = min(range(len(week_starts)), key=lambda i: abs((week_starts[i] - intervention_start_date).days))
intervention_end_pos = min(range(len(week_starts)), key=lambda i: abs((week_starts[i] - intervention_end_date).days))
ax.axvspan(intervention_start_pos - 0.5, intervention_end_pos - 0.5, color=intervention_box_color, alpha=1, zorder=0, label='Intervention period (eight weeks)')

# highlight IQR (101-171 days) period after 20.02.2024
day_101 = pd.Timestamp('2024-02-20') + pd.Timedelta(days=101)
day_171 = pd.Timestamp('2024-02-20') + pd.Timedelta(days=171)
# find closest week_starts indices for the IQR start and end dates
blue_start_index = min(range(len(week_starts)), key=lambda i: abs((week_starts[i] - day_101).days))
blue_end_index = min(range(len(week_starts)), key=lambda i: abs((week_starts[i] - day_171).days))
ax.axvspan(blue_start_index - 0.5, blue_end_index - 0.5, color=IQR_box_color, alpha=1, zorder=0, label='IQR (101-171 days) after 20/02/2024')

# print out the start and end dates of the IQR window box
print(f"IQR window box: Start date: {day_101.strftime('%d/%m/%Y')}, End date: {day_171.strftime('%d/%m/%Y')}")

# add vertical dashed line on 20.02.2024 and add to legend
line_date = pd.Timestamp('2024-02-20')
closest_index = min(range(len(week_starts)), key=lambda i: abs((week_starts[i] - line_date).days))
ax.axvline(x=closest_index, color=vertical_line_color, linestyle='--', linewidth=2, label='Midpoint of intervention: 20/02/2024')

# debugging information for verification
print(f"Intervention start date: {intervention_start_date}, Position: {intervention_start_pos}")
print(f"Intervention end date: {intervention_end_date}, Position: {intervention_end_pos}")
print(f"IQR start index: {blue_start_index}")
print(f"IQR end index: {blue_end_index}")

# reorder the legend entries
handles, labels = ax.get_legend_handles_labels()
desired_order = ['2022', '2023', '2024', 'Intervention period (eight weeks)', 'Midpoint of intervention: 20/02/2024', 'IQR (101-171 days) after 20/02/2024']
ordered_handles = []
ordered_labels = []
for label in desired_order:
    for h, l in zip(handles, labels):
        if l == label:
            ordered_handles.append(h)
            ordered_labels.append(l)
            break

plt.legend(ordered_handles, ordered_labels, fontsize=legend_fontsize, loc=legend_loc)

plt.title('Number of inner northwest cases by week for 2022, 2023 and 2024', fontsize=title_fontsize)
plt.xlabel('Day/Month', fontsize=xlabel_fontsize)
plt.ylabel('Number of cases', fontsize=ylabel_fontsize)
plt.xticks(fontsize=xtick_fontsize)
plt.yticks(fontsize=ytick_fontsize)
plt.tight_layout()

plt.savefig('Fig1_A.svg', format='svg')
plt.savefig('Fig1_A.png', format='png')

plt.show()
