# Thiết Kế Thí Nghiệm

## Mục Tiêu

Mục tiêu của dự án là đánh giá khả năng dự báo traffic được sinh bởi simulator và
lựa chọn Forecast Module phù hợp cho V2 Predictive RL.

Dự án không tập trung vào Reinforcement Learning mà chỉ tập trung vào bài toán
forecasting.

## Dataset

### Nguồn Dữ Liệu

Dữ liệu được sinh trực tiếp từ simulator của đồ án chính.

Scenario hiện tại:

- Indoor Hotspot

Dataset được tạo bằng cách chạy nhiều episode và ghi lại trạng thái traffic theo
thời gian.

### Feature

Các feature đầu vào:

| Feature | Mô tả |
|---|---|
| `traffic_load` | Tải mạng hiện tại |
| `ue_count` | Số lượng người dùng |
| `traffic_demand_bps` | Nhu cầu traffic |
| `mobility_event` | Sự kiện di chuyển |
| `time_ratio` | Vị trí tương đối trong episode |

### Target

Các target dự báo:

| Target | Ý nghĩa |
|---|---|
| `traffic_load_t_plus_1` | Dự báo bước tiếp theo |
| `traffic_load_t_plus_5` | Dự báo sau 5 bước |
| `traffic_load_t_plus_10` | Dự báo sau 10 bước |

## Data Split

Dataset được chia:

- 80% train
- 20% test

Split mặc định theo `episode_id` để test set không trùng episode với train set.

## Evaluation Metric

Các model được đánh giá bằng:

### MAE

Mean Absolute Error, dùng để đo sai số tuyệt đối trung bình.

### RMSE

Root Mean Squared Error, dùng để đo mức sai lệch lớn.

### R²

R² score, dùng để đo mức độ model giải thích biến động của dữ liệu.

## Thí Nghiệm 1

### Forecast Horizon Analysis

Mục tiêu là đánh giá khả năng dự báo ở các horizon khác nhau.

Các mốc:

- `t+1`
- `t+5`
- `t+10`

Câu hỏi: sai số có tăng nhanh khi horizon dài hơn hay không?

## Thí Nghiệm 2

### Feature Contribution Analysis

Mục tiêu là đánh giá ảnh hưởng của từng nhóm feature.

### Feature Set A

`traffic_load`

### Feature Set B

`traffic_load`, `ue_count`

### Feature Set C

`traffic_load`, `ue_count`, `traffic_demand_bps`, `mobility_event`, `time_ratio`

Câu hỏi: thông tin ngoài traffic hiện tại có giúp cải thiện khả năng dự báo hay
không?

## Thí Nghiệm 3

### History Window Analysis

Mục tiêu là đánh giá lượng lịch sử cần thiết cho dự báo.

Các cấu hình:

- Window = 5
- Window = 10
- Window = 20
- Window = 30

Câu hỏi: bao nhiêu bước lịch sử là đủ để dự báo traffic?

## Thí Nghiệm 4

### Model Benchmark

Mục tiêu là so sánh hiệu năng giữa các model.

Các model:

- Linear Regression: baseline đơn giản.
- Random Forest: model benchmark tiếp theo.
- Công việc tương lai: XGBoost, GRU, LSTM.

## Tóm Tắt Kết Quả Cần Có

Kết quả cuối cùng cần trả lời:

- Traffic simulator có khả năng dự báo hay không?
- Forecast Horizon nào phù hợp nhất?
- Feature nào quan trọng nhất?
- Model nào phù hợp nhất?
- Pipeline nào sẽ được tích hợp vào V2 Predictive RL?
