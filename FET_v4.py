import pandas as pd
import numpy as np
from geopy.distance import geodesic
from scipy.stats import fisher_exact
import sys
from statsmodels.stats.proportion import proportion_confint

# Set the zone radius (in km)
ZONE_RADIUS_KM = 0.8 

# calculate Haversine distances
def haversine_distances(sample_coords, site_coords):
    return np.array([
        [geodesic((lat1, lon1), (lat2, lon2)).km for lat2, lon2 in site_coords]
        for lat1, lon1 in sample_coords
    ])

# compute Fisher’s exact test for a given start and end unix time
def main(cases_file, treatment_sites_file, control_sites_file, start_unix, end_unix):
    # Load data
    cases = pd.read_csv(cases_file)
    treatment_sites = pd.read_csv(treatment_sites_file)
    control_sites = pd.read_csv(control_sites_file)

    # convert unix_time column to numeric
    cases["unix_time"] = pd.to_numeric(cases["unix_time"], errors="coerce")

    # filter cases within a specified time window
    cases_window = cases[(cases['unix_time'] >= start_unix) & (cases['unix_time'] <= end_unix)].copy()

    if cases_window.empty:
        print("No cases found in the specified time window.")
        return

    # convert lat/lon to numpy arrays
    treatment_coords = treatment_sites[['lat', 'lon']].to_numpy()
    control_coords = control_sites[['lat', 'lon']].to_numpy()

    # compute distances to treatment and control sites
    treatment_distances = haversine_distances(cases_window[['lat', 'lon']].to_numpy(), treatment_coords)
    control_distances = haversine_distances(cases_window[['lat', 'lon']].to_numpy(), control_coords)

    # assign each case to the nearest zone (treatment or control)
    cases_window['nearest_zone'] = np.where(
        treatment_distances.min(axis=1) < control_distances.min(axis=1), 'Treatment', 'Control'
    )

    # determine if cases are within the treatment or control zone
    cases_window['within_treatment_zone'] = (treatment_distances.min(axis=1) <= ZONE_RADIUS_KM).astype(int)
    cases_window['within_control_zone'] = (control_distances.min(axis=1) <= ZONE_RADIUS_KM).astype(int)

    # count cases within each zone
    treatment_counts = cases_window[cases_window['nearest_zone'] == 'Treatment']['within_treatment_zone'].value_counts().reindex([1, 0], fill_value=0)
    control_counts = cases_window[cases_window['nearest_zone'] == 'Control']['within_control_zone'].value_counts().reindex([1, 0], fill_value=0)

    # total number of unique cases in the window
    total_cases_in_window = cases_window.shape[0]

    # make contingency table
    # table layout:
    #         Inside Zone    Outside Zone
    # treatment   a                c
    # control     b                d
    a = treatment_counts[1]
    b = control_counts[1]
    c = treatment_counts[0]
    d = control_counts[0]
    contingency_table = np.array([[a, b],
                                  [c, d]])

    # check for zero counts in the table (for row or column totals)
    if np.any(contingency_table.sum(axis=0) == 0) or np.any(contingency_table.sum(axis=1) == 0):
        print("Insufficient data for Fisher’s Exact Test (zero counts in contingency table).")
        return

    # do Fisher’s exact test
    odds_ratio_fisher, p_value = fisher_exact(contingency_table)

    # use exact method from statsmodels for odds ratio and the 95% CI
    from statsmodels.stats.contingency_tables import Table2x2
    table2x2 = Table2x2(contingency_table)
    odds_ratio = table2x2.oddsratio
    ci_lower, ci_upper = table2x2.oddsratio_confint(alpha=0.05)

    # estimate the number of cases prevented using the proportion-based method
    total_control_cases = b + d
    total_treatment_cases = a + c

    if total_control_cases > 0:
        # p_control is the observed proportion in the control zone
        p_control = b / total_control_cases
        expected_cases_treatment = p_control * total_treatment_cases
        cases_prevented = expected_cases_treatment - a

        # compute 95% CI for the control proportion
        ci_low_p, ci_upp_p = proportion_confint(count=b, nobs=total_control_cases, alpha=0.05, method='beta')
        # convert to expected cases in the treatment zone
        expected_cases_treatment_low = ci_low_p * total_treatment_cases
        expected_cases_treatment_upp = ci_upp_p * total_treatment_cases
        # do this for cases prevented
        cases_prevented_low = expected_cases_treatment_low - a
        cases_prevented_upp = expected_cases_treatment_upp - a
    else:
        expected_cases_treatment = np.nan
        cases_prevented = np.nan
        expected_cases_treatment_low = np.nan
        expected_cases_treatment_upp = np.nan
        cases_prevented_low = np.nan
        cases_prevented_upp = np.nan

    # interpretation of the odds ratio
    if odds_ratio < 1:
        interpretation = f"Cases inside the treatment zone are approximately {100 * (1 - odds_ratio):.1f}% less likely to occur within the IQR window compared to control."
    else:
        interpretation = f"Cases inside the treatment zone are approximately {100 * (odds_ratio - 1):.1f}% more likely to occur within the IQR window compared to control."

    # final summary statement
    final_statement = (
        f"If the intervention had no effect, we would expect approximately {expected_cases_treatment:.1f} cases in the treatment zone "
        f"(95% CI: {expected_cases_treatment_low:.1f} - {expected_cases_treatment_upp:.1f}), but only {a} cases occurred. "
        f"This suggests that approximately {cases_prevented:.1f} cases were prevented due to the intervention "
        f"(95% CI: {cases_prevented_low:.1f} - {cases_prevented_upp:.1f})."
    )

    # print results
    print("Fisher’s Exact Test Results:")
    print("----------------------------------------------------")
    print("Cases Inside Treatment Zone:", a)
    print("Cases Outside Treatment Zone:", c)
    print("Cases Inside Control Zone:", b)
    print("Cases Outside Control Zone:", d)
    print("Total Unique Cases in Window:", total_cases_in_window)
    print("----------------------------------------------------")
    print(f"Odds Ratio: {odds_ratio:.3f} (95% CI: {ci_lower:.3f} - {ci_upper:.3f})")
    print(f"P-value: {p_value:.5f}")
    print(f"Cases Prevented: {cases_prevented:.1f} (95% CI: {cases_prevented_low:.1f} - {cases_prevented_upp:.1f})")
    print(f"Interpretation: {interpretation}")
    print(final_statement)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <cases_file> <treatment_sites_file> <control_sites_file> <start_unix> <end_unix>")
        sys.exit(1)

    cases_file = sys.argv[1]
    treatment_sites_file = sys.argv[2]
    control_sites_file = sys.argv[3]
    start_unix = int(sys.argv[4])
    end_unix = int(sys.argv[5])

    main(cases_file, treatment_sites_file, control_sites_file, start_unix, end_unix)
