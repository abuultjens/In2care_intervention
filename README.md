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
Contingency Table:
|             | Inside Zone | Outside Zone |
|-------------|-------------|--------------|
| Treatment   | a = 0       | c = 13       |
| Control     | b = 7       | d = 7        |

This analysis uses `statsmodels`, which applies a continuity correction internally
to avoid issues with zero counts. Specifically, it uses the **Haldane–Anscombe correction**,
adding 0.5 to cells with zero counts in the table before calculating the odds ratio.

```python
from statsmodels.stats.contingency_tables import Table2x2

table2x2 = Table2x2(contingency_table)
odds_ratio = table2x2.oddsratio

The equation is then:
OR=((b+0.5)/(c+0))/((a+0)/(d+0))
OR=((0+0.5)/(c+13))/((a+7)/(d+7))
OR=0.038
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





