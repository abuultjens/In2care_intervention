# In2care_intervention

# Dependencies:
```
dateutil==2.8.2
geopy==2.4.0
matplotlib==3.7.1
scipy==1.9.1
shapely==2.0.2
statsmodels==0.13.2
contextily==1.6.2
geopandas==1.0.1
numpy==1.26.4
pandas==2.2.3
```

## Make epidemiological plot (Fig. 1A):
```
python year_alignment_plot_v2_trend_lines_v2.py
```

## Make mapping plot (Fig. 1B):
```
python Fig_1_v7.py
This requires the ESRI shapefile format files from the Australian Bureau of Statistics (update line 94 with path to these files):
https://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&1270055001_mb_2011_vic_shape.zip&1270.0.55.001&Data%20Cubes&85F5B2ED8E3DC957CA257801000CA953&0&July%202011&23.12.2010&Latest

```

## Calculate Fisher's exact test for specific time window
```
python FET_v4.py [cases_file] [treatment_sites_file] [control_sites_file] [start_unix] [end_unix]
python FET_v4.py Inner_northwest_2024_cases_symptom.csv Treatment_lat_lon.csv Control_lat_lon.csv 1718715600 1724850000

```

### How the odd's ratio is calculated:
Example contingency Table:
|             | Inside Zone | Outside Zone |
|-------------|-------------|--------------|
| Treatment   | a = 0       | c = 13       |
| Control     | b = 7       | d = 7        |

This analysis uses `statsmodels`, which applies a continuity correction internally
to avoid issues with zero counts. Specifically, it uses the **Haldane–Anscombe correction**,
adding 0.5 to cells with zero counts in the table before calculating the odds ratio.

```python
from statsmodels.stats.contingency_tables import Table2x2

# Create the contingency table
table2x2 = Table2x2(contingency_table)

# Compute the odds ratio
odds_ratio = table2x2.oddsratio

The equation is:
Odds Ratio = ((a + 0.5) / (c + 0)) / ((b + 0) / (d + 0))
Odds Ratio = ((0.5) / (13)) / ((7) / (7))
Odds Ratio = 0.038
```

### How the odd's ration 95% confidence intervals are calculated:

```
  python
from statsmodels.stats.contingency_tables import Table2x2

# Create the contingency table
table2x2 = Table2x2(contingency_table)

# Compute the odds ratio and 95% confidence interval
odds_ratio = table2x2.oddsratio
ci_lower, ci_upper = table2x2.oddsratio_confint(alpha=0.05)

Equations:
Standard error = sqrt(1/a + 1/b + 1/c + 1/d)
Standard error = sqrt(1/0.5 + 1/7 + 1/13 + 1/7)
Standard error = 1.537

log(OR) = log(0.038) = -3.27

Lower log bound = -3.27 - 1.96 × 1.537
Lower log bound = -6.28
Lower = exp(-6.28)
Lower = 0.0019

Upper log bound = -3.27 + 1.96 × 1.537
Upper log bound = -0.257
Upper = exp(-0.257)
Upper = 0.7734

Final 95% CI for Odds Ratio: (0.0019, 0.7734)
```

### How the cases prevented are calculated:
The question being asked:
“If the treatment zone had the same proportion of cases as the control zone, how many cases would we have expected to see in the treatment zone? And how many were prevented compared to that expectation?”

Example contingency Table:
|             | Inside Zone | Outside Zone |
|-------------|-------------|--------------|
| Treatment   | a = 0       | c = 13       |
| Control     | b = 7       | d = 7        |

```
Cases prevented = (b / (b + d)) * (a + c) - a
Cases prevented = (7 / (7 + 7)) * (0 + 13) - 0
Cases prevented = 6.5
```

### How the cases prevented 95% confidence intervals are calculated:
```
With the code:
from statsmodels.stats.proportion import proportion_confint
ci_low_p, ci_upp_p = proportion_confint(count=b, nobs=b + d, alpha=0.05, method='beta')

Equations:
cases_prevented_lower = ((b / (b + d)) - 1.96 × sqrt((b / (b + d)) × (1 - (b / (b + d))) / (b + d))) × (a + c) - a
cases_prevented_lower = ((7 / (7 + 7)) - 1.96 × sqrt((7 / (7 + 7)) × (1 - (7 / (7 + 7))) / (7 + 7))) × (0 + 13) - 0
cases_prevented_lower = 3.09

cases_prevented_upper = ((b / (b + d)) + 1.96 × sqrt((b / (b + d)) × (1 - (b / (b + d))) / (b + d))) × (a + c) - a
cases_prevented_upper = ((7 / (7 + 7)) + 1.96 × sqrt((7 / (7 + 7)) × (1 - (7 / (7 + 7))) / (7 + 7))) × (0 + 13) - 0
cases_prevented_upper = 9.90
```


## Make sliding window case counts plot (Fig. 3A):
```
python Counts_plot_v3.py
```

## Make sliding window p-value plot (Fig. 3B):
```
python sliding_window_density_pval_date_cutoff_zone_v2-egg-count_v5.py
```

## Make sliding window egg count and cases prevented plot (Fig. 3C):
```
python Timeplot_of_egg-count-diff_and_treat_mean-diff_v4.py
```

## Compare imputed egg counts with actual 2022 egg counts (Fig. SX):
```
python Comparing_imputed_vs_2022_mozzie_data.py
```





