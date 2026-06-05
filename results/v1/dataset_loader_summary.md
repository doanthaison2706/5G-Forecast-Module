# V1 M1 Dataset Loader Summary

This file is the official milestone artifact for V1 M1 Dataset Loader.

## Dataset Split

- Total dataset rows: 29,000
- Train rows: 23,200
- Test rows: 5,800
- Train/test ratio: 80.00% / 20.00%

## Features

- Feature count: 7
- Feature names:
  - `traffic_load`
  - `ue_count`
  - `traffic_demand_bps`
  - `time_ratio`
  - `mobility_event_busy_period`
  - `mobility_event_crowd_surge`
  - `mobility_event_normal`

## Forecast Targets

- Available forecast targets:
  - `t+1` -> `traffic_load_t_plus_1`
  - `t+5` -> `traffic_load_t_plus_5`
  - `t+10` -> `traffic_load_t_plus_10`

## Validation

- Validation status: PASS
- Validation checks passed: 13/13
