import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta

# Y-axis ranges
treatment_control_y_range = (0, 20)  
total_y_range = (0, 38) 

# line thickness
TREATMENT_LINE_THICKNESS = 4
CONTROL_LINE_THICKNESS = 4
TOTAL_LINE_THICKNESS = 4
VERTICAL_LINE_THICKNESS = 2

# line colors 
TREATMENT_LINE_COLOR = '#D55E00' 
CONTROL_LINE_COLOR = '#56B4E9' 
TOTAL_LINE_COLOR = '#E69F00' 
VERTICAL_LINE_COLOR = '#0072B2' 

# font sizes
AXES_NUMBER_SIZE = 20
AXIS_LABEL_FONT_SIZE = 20  
PLOT_TITLE_SIZE = 21  
LEGEND_FONT_SIZE = 13  

# font size of legend text
LEGEND_TEXT_FONT_SIZE = 15

# font size of the x and y axis labels
X_AXIS_LABEL_FONT_SIZE = 20
Y_AXIS_LABEL_FONT_SIZE = 20

# horizontal offset for the left y-axis label
Y_AXIS_LABEL_PAD = 10

# horizontal offset for the right y-axis label
RIGHT_Y_AXIS_LABEL_PAD = 10

# legend position coordinates
LEGEND_X = -0.007 
LEGEND_Y = 1.02

# X-axis tick mark interval
X_AXIS_TICK_INTERVAL = 5  

# dates for vertical dotted lines
highlight_dates = ["25.01.2024", "21.03.2024"]

# load the CSV file
file_path = '4.5-DATE_Essendon_2024_all_symptom_date_70_treatment_sliding_window_Haversine_800m_FET_v1-PVAL-OR-CP_IN-OUT_report.csv'
df = pd.read_csv(file_path)

# convert timestamp to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True, errors='coerce')

# find timestamps that match the highlight dates
highlight_indices = df[df['Timestamp'].dt.strftime('%d.%m.%Y').isin(highlight_dates)].index.tolist()

# plot the data
fig, ax1 = plt.subplots(figsize=(12, 5.5))

# primary y-axis for zones
line1, = ax1.plot(df['Timestamp'], df['In treatment zone'], label='Cases in treatment zones (left y-axis)', color=TREATMENT_LINE_COLOR, linewidth=TREATMENT_LINE_THICKNESS)
line2, = ax1.plot(df['Timestamp'], df['In control zone'], label='Cases in control zones (left y-axis)', color=CONTROL_LINE_COLOR, linewidth=CONTROL_LINE_THICKNESS)

ax1.set_ylabel('Number of cases per window', fontsize=Y_AXIS_LABEL_FONT_SIZE, labelpad=Y_AXIS_LABEL_PAD)
ax1.set_ylim(treatment_control_y_range)
ax1.tick_params(axis='y', labelsize=AXES_NUMBER_SIZE)

# rotate x-axis labels 
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=X_AXIS_TICK_INTERVAL))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
plt.xticks(rotation=45, ha='right')

# add vertical dotted lines
for idx in highlight_indices:
    ax1.axvline(x=df['Timestamp'].iloc[idx], color=VERTICAL_LINE_COLOR, linestyle='dashed', linewidth=VERTICAL_LINE_THICKNESS)

# secondary y-axis for TOTAL
ax2 = ax1.twinx()
line3, = ax2.plot(df['Timestamp'], df['TOTAL'], label='Total cases per window (right y-axis)', color=TOTAL_LINE_COLOR, linestyle='-', linewidth=TOTAL_LINE_THICKNESS)
ax2.set_ylabel('Total cases per window', fontsize=Y_AXIS_LABEL_FONT_SIZE, color=TOTAL_LINE_COLOR, labelpad=RIGHT_Y_AXIS_LABEL_PAD)
ax2.set_ylim(total_y_range)
ax2.tick_params(axis='y', labelsize=AXES_NUMBER_SIZE, colors=TOTAL_LINE_COLOR)

# combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()

# add vertical line to the legend only once
vertical_line_legend = plt.Line2D([], [], color=VERTICAL_LINE_COLOR, linestyle='dashed', linewidth=VERTICAL_LINE_THICKNESS, label='Start/end of intervention')

# combine handles and labels
handles = lines_1 + lines_2 + [vertical_line_legend]
labels = labels_1 + labels_2 + ['Start/end of intervention']

# set legend position based on coordinates
ax1.legend(handles, labels, loc='upper left', bbox_to_anchor=(LEGEND_X, LEGEND_Y), fontsize=LEGEND_TEXT_FONT_SIZE)

# Add faint vertical and horizontal grid lines
ax1.grid(alpha=0.3)

plt.title('Raw Case Counts in Treatment and Control Zones', fontsize=PLOT_TITLE_SIZE)
plt.tight_layout()

# save the figure
plt.savefig('Fig3_A.svg', format='svg')
plt.savefig('Fig3_A.png', format='png')

plt.show()
