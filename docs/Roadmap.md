# ROADMAP

## Mục tiêu dự án

Xây dựng và đánh giá Forecast Module phục vụ cho V2 Predictive RL.

---

# Version Plan

## V0 — Dataset Validation

### Objective

Kiểm tra chất lượng dataset được sinh từ simulator.

### Scope

- Làm sạch dữ liệu
- Khám phá dữ liệu
- Thống kê cơ bản
- Kiểm tra phân phối traffic

### Deliverables

- Dataset Summary
- Dataset Visualization

### Success Criteria

- Dataset hợp lệ
- Không có lỗi dữ liệu nghiêm trọng
- Có thể sử dụng cho bài toán dự báo

---

## V1 — Baseline Forecast

### Objective

Xây dựng mô hình dự báo cơ bản.

### Scope

- Linear Regression
- Train/Test Pipeline
- MAE
- RMSE
- R²

### Success Criteria

- Pipeline huấn luyện hoàn chỉnh
- Có baseline để so sánh

---

## V2 — Forecast Benchmark

### Objective

So sánh nhiều cấu hình dự báo khác nhau.

### Scope

### Horizon Analysis

- t + 1
- t + 5
- t + 10

### Window Analysis

- Window 5
- Window 10
- Window 20
- Window 30

### Feature Analysis

- Traffic Only
- Traffic + UE
- Full Features

### Model Comparison

- Linear Regression
- Random Forest

### Success Criteria

- Xác định được cấu hình tốt nhất
- Xác định được mô hình tốt nhất

---

## V3 — Forecast Module Release

### Objective

Đóng gói Forecast Module để sử dụng trong đồ án chính.

### Scope

- Lưu model
- Inference Pipeline
- Module Integration Interface

### Output

PredictedTrafficLoad(t+1)

PredictedTrafficLoad(t+5)

PredictedTrafficLoad(t+10)

### Success Criteria

- Có thể tích hợp trực tiếp vào V2 Predictive RL
- Kết quả dự báo được xuất dưới dạng Forecast State

---

# Kết quả mong đợi

Sau khi hoàn thành dự án:

- Xác định được khả năng dự báo của traffic simulator.
- Lựa chọn được Forecast Pipeline phù hợp.
- Chuẩn bị Forecast Module cho V2 Predictive RL.

---

# Liên hệ với đồ án chính

Roadmap tổng thể:

V0 → Reactive RL

V1 → Predictive RL với Oracle Forecast

V2 → Predictive RL với Learned Forecast

Dự án này tập trung vào việc xây dựng thành phần Learned Forecast trước khi tích hợp vào V2.