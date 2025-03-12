# In2care_intervention

## make epidemiological plot (Fig. 1A)
```
python year_alignment_plot_v2_trend_lines_v2.py
```

## Calculate Fisher's exact test for specific time window
```
python FET_v4.py [cases_file] [treatment_sites_file] [control_sites_file] [start_unix] [end_unix]
python FET_v4.py Inner_northwest_2024_cases_symptom.csv Treatment_lat_lon.csv Control_lat_lon.csv 1718715600 1724850000

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





