# V0 Dataset Validation Report

Overall status: **PASS**

## Dataset

- Rows: 29000
- Columns: 10
- Episodes: 100
- Rows per episode: min=290, max=290, mean=290.00

## Checks

| Check | Status | Details |
|---|---:|---|
| required_columns | PASS | All required columns are present. |
| missing_values | PASS | Total missing values: 0 |
| duplicate_rows | PASS | Duplicate rows: 0 |
| traffic_range | PASS | Rows outside [0, 1]: {'traffic_load': 0, 'traffic_load_t_plus_1': 0, 'traffic_load_t_plus_5': 0, 'traffic_load_t_plus_10': 0} |
| ue_count_range | PASS | Rows with negative ue_count: 0 |
| traffic_demand_range | PASS | Rows with negative traffic_demand_bps: 0 |
| time_ratio_range | PASS | Rows outside [0, 1]: 0 |
| episode_step_duplicates | PASS | Duplicate episode-step pairs: 0 |
| episode_step_order | PASS | Episodes not sorted by step: 0 |
| episode_step_continuity | PASS | Episodes with missing steps: 0 |
| traffic_load_t_plus_1_alignment | PASS | Comparable rows: 28900; mismatches: 0 |
| traffic_load_t_plus_5_alignment | PASS | Comparable rows: 28500; mismatches: 0 |
| traffic_load_t_plus_10_alignment | PASS | Comparable rows: 28000; mismatches: 0 |

## V0 Conclusion

The dataset is suitable for V1 baseline forecasting if all checks pass.
Target alignment is checked where the future step is available within the exported dataset.
