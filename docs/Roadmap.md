# Roadmap

## Mục Tiêu Dự Án

Xây dựng và đánh giá Forecast Module phục vụ cho V2 Predictive RL.

## Kế Hoạch Theo Version

## V0 - Dataset Validation

### Mục Tiêu

Kiểm tra chất lượng dataset được sinh từ simulator.

### Phạm Vi

- Làm sạch dữ liệu.
- Khám phá dữ liệu.
- Thống kê cơ bản.
- Kiểm tra phân phối traffic.

### Artifact

- Dataset Summary.
- Dataset Visualization.
- Validation Report.

### Tiêu Chí Thành Công

- Dataset hợp lệ.
- Không có lỗi dữ liệu nghiêm trọng.
- Có thể sử dụng cho bài toán forecasting.

## V1 - Baseline Forecast

### Mục Tiêu

Xây dựng model dự báo cơ bản.

### Phạm Vi

- M1 Dataset Loader.
- M2 Feature Set Definition.
- M3 Linear Regression Baseline.
- Train/Test Pipeline.
- MAE, RMSE, R².

### Tiêu Chí Thành Công

- Pipeline train hoàn chỉnh.
- Có baseline để so sánh.
- Có artifact cho từng milestone.

## V2 - Forecast Benchmark

### Mục Tiêu

So sánh nhiều cấu hình dự báo khác nhau.

### Horizon Analysis

- `t+1`
- `t+5`
- `t+10`

### Window Analysis

- Window 5.
- Window 10.
- Window 20.
- Window 30.

### Feature Analysis

- Traffic Only.
- Traffic + UE.
- Full Features.

### Model Comparison

- Linear Regression.
- Random Forest.

### Tiêu Chí Thành Công

- Xác định được cấu hình tốt nhất.
- Xác định được model tốt nhất.

## V3 - Forecast Module Release

### Mục Tiêu

Đóng gói Forecast Module để sử dụng trong đồ án chính.

### Phạm Vi

- Lưu model.
- Inference Pipeline.
- Module Integration Interface.

### Kết Quả Output

- `PredictedTrafficLoad(t+1)`
- `PredictedTrafficLoad(t+5)`
- `PredictedTrafficLoad(t+10)`

### Tiêu Chí Thành Công

- Có thể tích hợp trực tiếp vào V2 Predictive RL.
- Kết quả dự báo được xuất dưới dạng Forecast State.

## Kết Quả Mong Đợi

Sau khi hoàn thành dự án:

- Xác định được khả năng dự báo của traffic simulator.
- Lựa chọn được Forecast Pipeline phù hợp.
- Chuẩn bị Forecast Module cho V2 Predictive RL.

## Liên Hệ Với Đồ Án Chính

Roadmap tổng thể:

- V0 -> Reactive RL.
- V1 -> Predictive RL với Oracle Forecast.
- V2 -> Predictive RL với Learned Forecast.

Dự án này tập trung vào việc xây dựng thành phần Learned Forecast trước khi tích
hợp vào V2.
