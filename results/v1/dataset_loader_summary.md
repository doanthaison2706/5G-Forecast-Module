# V1 M1 Tóm Tắt Dataset Loader

File này là artifact chính thức cho V1 M1 Dataset Loader.

## Chia Dataset

- Tổng số dòng dataset: 29,000
- Số dòng train: 23,200
- Số dòng test: 5,800
- Tỷ lệ train/test: 80.00% / 20.00%

## Feature

- Số lượng feature: 7
- Tên feature:
  - `traffic_load`
  - `ue_count`
  - `traffic_demand_bps`
  - `time_ratio`
  - `mobility_event_busy_period`
  - `mobility_event_crowd_surge`
  - `mobility_event_normal`

## Forecast Target

- Forecast target khả dụng:
  - `t+1` -> `traffic_load_t_plus_1`
  - `t+5` -> `traffic_load_t_plus_5`
  - `t+10` -> `traffic_load_t_plus_10`

## Validation

- Trạng thái validation: PASS
- Số check validation đạt: 13/13
