import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Load file
file_path = 'Comparing_imputed_vs_2022_mozzie_data.csv'
df = pd.read_csv(file_path)

# sort
sorted_df = df.sort_values(by='ABS_DIFF_IMPUTED')

# convert columns to float 
x = sorted_df['ABS_DIFF_IMPUTED'].astype('float64').values
y = sorted_df['ABS_DIFF_2022_DATA'].astype('float64').values

# linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
predicted_sorted = slope * x + intercept

# calculate confidence interval
n = len(df)
mean_x = np.mean(x)
t_val = stats.t.ppf(0.975, df=n-2)  # 95% CI
se = np.sqrt(np.sum((y - predicted_sorted) ** 2) / (n - 2))
conf_interval_sorted = t_val * se * np.sqrt(1/n + (x - mean_x)**2 / np.sum((x - mean_x)**2))

# plot with black data points and confidence interval
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color='black', label='Data Points')  # Black data points
plt.plot(x, predicted_sorted, color='red', label=f'Fit Line (R²={r_value**2:.2f}, p={p_value:.3f})')

# add confidence interval as a shaded area
plt.fill_between(x, 
                 predicted_sorted - conf_interval_sorted, 
                 predicted_sorted + conf_interval_sorted, 
                 color='red', alpha=0.2, label='95% CI')

# labels and title
plt.xlabel('Imputed egg count differences during In2care intervention 2024')
plt.ylabel('Actual egg count differences during In2care intervention 2022')
plt.title('Scatterplot with Linear Regression Line and 95% CI')
plt.legend()

plt.tight_layout()
plt.show()
