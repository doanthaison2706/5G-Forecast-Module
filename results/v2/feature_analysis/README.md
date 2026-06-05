# V2 Experiment 3 - Feature Contribution Analysis

Mục tiêu của thí nghiệm này là đánh giá thông tin ngoài traffic hiện tại có giúp cải thiện dự báo hay không.

## Cấu Hình Cố Định

- Model: `linear_regression`
- Target horizon: `t+1`
- Train/test split: 80/20 theo `episode_id`
- Feature set so sánh: `traffic_only`, `traffic_ue`, `full_features`

## Feature Set

| Feature set | Raw feature | Mô tả |
|---|---|---|
| `traffic_only` | `traffic_load` | Chỉ dùng traffic hiện tại làm baseline autoregressive tối thiểu. |
| `traffic_ue` | `traffic_load`, `ue_count` | Thêm UE count để kiểm tra mật độ người dùng có cải thiện dự báo không. |
| `full_features` | `traffic_load`, `ue_count`, `traffic_demand_bps`, `mobility_event`, `time_ratio` | Dùng toàn bộ feature baseline V1 có sẵn trước bước train model. |

## Kết Quả Train/Predict

| Feature set | Horizon | Raw feature | Encoded feature | Dòng train | Dòng predict | MAE | RMSE | R² |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `traffic_only` | t+1 | 1 | 1 | 23,200 | 5,800 | 0.038725 | 0.048663 | 0.909454 |
| `traffic_ue` | t+1 | 2 | 2 | 23,200 | 5,800 | 0.038724 | 0.048668 | 0.909438 |
| `full_features` | t+1 | 5 | 7 | 23,200 | 5,800 | 0.038548 | 0.048478 | 0.910143 |

## Feature Diagnostics

| Feature set | MAE | RMSE | R² | MAE đổi so với traffic_only | RMSE đổi so với traffic_only | R² tăng so với traffic_only | MAE đổi so với set trước | Quyết định |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `traffic_only` | 0.038725 | 0.048663 | 0.909454 | 0.000000 | 0.000000 | 0.000000 | n/a | `recommended` |
| `traffic_ue` | 0.038724 | 0.048668 | 0.909438 | -0.000001 | 0.000004 | -0.000016 | -0.000001 | `recommended` |
| `full_features` | 0.038548 | 0.048478 | 0.910143 | -0.000176 | -0.000185 | 0.000689 | -0.000175 | `recommended` |

## Nhận Định

- Feature set tốt nhất theo MAE/RMSE là `full_features`.
- Feature set gọn nhất đạt mức recommended là `traffic_only`.
- Nếu feature ngoài traffic hiện tại không giảm sai số rõ rệt, V2 nên ưu tiên feature set nhỏ để giữ Forecast State đơn giản.

Figure đã tạo:

- `results/v2/feature_analysis/figures/linear_regression_metrics_by_feature_set.png`
- `results/v2/feature_analysis/figures/linear_regression_actual_vs_prediction.png`
- `results/v2/feature_analysis/figures/linear_regression_residual_distribution.png`
- `results/v2/feature_analysis/figures/linear_regression_sample_timeseries.png`

## Artifact

- Report: `results/v2/feature_analysis/README.md`
- Metric CSV: `results/v2/feature_analysis/feature_metrics.csv`
- Prediction CSV: `results/v2/feature_analysis/feature_predictions.csv`
- Figure: `results/v2/feature_analysis/figures/`

## Kết Luận

- Feature set được đề xuất cho V2 hiện tại: `traffic_only`.
- Có thể chuyển sang V2 Experiment 4 - Model Comparison.
