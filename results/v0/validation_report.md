# Báo Cáo Validation Dataset V0

Trạng thái tổng thể: **PASS**

## Dataset

- Số dòng: 29000
- Số cột: 10
- Số episode: 100
- Số dòng mỗi episode: min=290, max=290, mean=290.00

## Check

| Check | Trạng thái | Chi tiết |
|---|---:|---|
| required_columns | PASS | Có đủ các cột bắt buộc. |
| missing_values | PASS | Tổng giá trị thiếu: 0 |
| duplicate_rows | PASS | Số dòng trùng lặp: 0 |
| traffic_range | PASS | Số dòng ngoài khoảng [0, 1]: {'traffic_load': 0, 'traffic_load_t_plus_1': 0, 'traffic_load_t_plus_5': 0, 'traffic_load_t_plus_10': 0} |
| ue_count_range | PASS | Số dòng có ue_count âm: 0 |
| traffic_demand_range | PASS | Số dòng có traffic_demand_bps âm: 0 |
| time_ratio_range | PASS | Số dòng ngoài khoảng [0, 1]: 0 |
| episode_step_duplicates | PASS | Số cặp episode-step trùng lặp: 0 |
| episode_step_order | PASS | Số episode không được sort theo step: 0 |
| episode_step_continuity | PASS | Số episode bị thiếu step: 0 |
| traffic_load_t_plus_1_alignment | PASS | Số dòng so sánh được: 28900; số mismatch: 0 |
| traffic_load_t_plus_5_alignment | PASS | Số dòng so sánh được: 28500; số mismatch: 0 |
| traffic_load_t_plus_10_alignment | PASS | Số dòng so sánh được: 28000; số mismatch: 0 |

## Kết Luận V0

Dataset phù hợp để chuyển sang V1 baseline forecasting khi tất cả check đều PASS.
Target alignment được kiểm tra ở các dòng có future step trong dataset đã export.
