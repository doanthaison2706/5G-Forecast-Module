# V1 M2 Định Nghĩa Feature Set

File này là artifact chính thức cho V1 M2 Feature Set Definition.

## Phạm Vi

Feature set xác định các cột đầu vào được dùng trong pipeline dự báo baseline V1.
Cột categorical được Dataset Loader chuyển thành cột numeric cho model.

## Feature Set Mặc Định

- Mặc định: `full_features`

## Forecast Target

- Forecast target khả dụng:
  - `t+1` -> `traffic_load_t_plus_1`
  - `t+5` -> `traffic_load_t_plus_5`
  - `t+10` -> `traffic_load_t_plus_10`

## Các Feature Set

### `traffic_only`

- Mô tả: Chỉ dùng traffic hiện tại làm baseline autoregressive tối thiểu.
- Số lượng raw feature: 1
- Tên raw feature:
  - `traffic_load`
- Số lượng encoded feature: 1
- Tên encoded feature:
  - `traffic_load`

### `traffic_ue`

- Mô tả: Thêm UE count để kiểm tra mật độ người dùng có cải thiện dự báo không.
- Số lượng raw feature: 2
- Tên raw feature:
  - `traffic_load`
  - `ue_count`
- Số lượng encoded feature: 2
- Tên encoded feature:
  - `traffic_load`
  - `ue_count`

### `full_features`

- Mô tả: Dùng toàn bộ feature baseline V1 có sẵn trước bước train model.
- Số lượng raw feature: 5
- Tên raw feature:
  - `traffic_load`
  - `ue_count`
  - `traffic_demand_bps`
  - `mobility_event`
  - `time_ratio`
- Số lượng encoded feature: 7
- Tên encoded feature:
  - `traffic_load`
  - `ue_count`
  - `traffic_demand_bps`
  - `time_ratio`
  - `mobility_event_busy_period`
  - `mobility_event_crowd_surge`
  - `mobility_event_normal`

## Validation

- Trạng thái định nghĩa feature set: PASS
- Tất cả feature set đã định nghĩa đều build được bằng V1 Dataset Loader.
