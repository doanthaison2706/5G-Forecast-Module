# EXPERIMENT DESIGN

## Mục tiêu

Mục tiêu của dự án là đánh giá khả năng dự báo traffic được sinh bởi simulator và lựa chọn Forecast Module phù hợp cho V2 Predictive RL.

Dự án không tập trung vào Reinforcement Learning mà chỉ tập trung vào bài toán dự báo.

---

# Dataset

## Nguồn dữ liệu

Dữ liệu được sinh trực tiếp từ simulator của đồ án chính.

Scenario hiện tại:

- Indoor Hotspot

Dataset được tạo bằng cách chạy nhiều Episode và ghi lại trạng thái traffic theo thời gian.

---

## Features

Các đặc trưng đầu vào:

| Feature | Mô tả |
|----------|----------|
| traffic_load | Tải mạng hiện tại |
| ue_count | Số lượng người dùng |
| traffic_demand_bps | Nhu cầu lưu lượng |
| mobility_event | Sự kiện di chuyển |
| time_ratio | Vị trí tương đối trong Episode |

---

## Target

Các mục tiêu dự báo:

| Target | Ý nghĩa |
|----------|----------|
| traffic_load_t_plus_1 | Dự báo bước tiếp theo |
| traffic_load_t_plus_5 | Dự báo sau 5 bước |
| traffic_load_t_plus_10 | Dự báo sau 10 bước |

---

# Data Split

Dataset được chia:

- 80% Training
- 20% Testing

Random State cố định để đảm bảo khả năng tái lập.

---

# Evaluation Metrics

Các mô hình được đánh giá bằng:

## MAE

Mean Absolute Error

Đánh giá sai số tuyệt đối trung bình.

---

## RMSE

Root Mean Squared Error

Đánh giá mức độ sai lệch lớn.

---

## R² Score

Đánh giá mức độ giải thích biến động của dữ liệu.

---

# Experiment 1

## Forecast Horizon Analysis

Mục tiêu:

Đánh giá khả năng dự báo ở các khoảng thời gian khác nhau.

Các mốc:

- t + 1
- t + 5
- t + 10

Câu hỏi:

Liệu sai số có tăng nhanh khi khoảng dự báo dài hơn hay không?

---

# Experiment 2

## Feature Contribution Analysis

Mục tiêu:

Đánh giá ảnh hưởng của từng nhóm đặc trưng.

### Feature Set A

traffic_load

### Feature Set B

traffic_load

ue_count

### Feature Set C

traffic_load

ue_count

traffic_demand_bps

mobility_event

time_ratio

Câu hỏi:

Thông tin ngoài traffic hiện tại có giúp cải thiện khả năng dự báo hay không?

---

# Experiment 3

## History Window Analysis

Mục tiêu:

Đánh giá lượng lịch sử cần thiết cho dự báo.

Các cấu hình:

- Window = 5
- Window = 10
- Window = 20
- Window = 30

Câu hỏi:

Bao nhiêu bước lịch sử là đủ để dự báo traffic?

---

# Experiment 4

## Model Benchmark

Mục tiêu:

So sánh hiệu năng giữa các mô hình.

Các mô hình:

### Linear Regression

Baseline đơn giản.

### Random Forest

Mô hình chính của phiên bản hiện tại.

### Future Work

- XGBoost
- GRU
- LSTM

---

# Result Summary

Kết quả cuối cùng cần trả lời:

- Traffic simulator có khả năng dự báo hay không?
- Forecast Horizon nào phù hợp nhất?
- Feature nào quan trọng nhất?
- Mô hình nào phù hợp nhất?
- Pipeline nào sẽ được tích hợp vào V2 Predictive RL?