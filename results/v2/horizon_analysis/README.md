# V2 Experiment 1 - Forecast Horizon Analysis

Mục tiêu của thí nghiệm này là kiểm tra sai số dự báo thay đổi như thế nào khi horizon dài hơn.

## Cấu Hình Cố Định

- Model: `linear_regression`
- Feature set: `full_features`
- Train/test split: 80/20 theo `episode_id`
- Horizon so sánh: `t+1`, `t+5`, `t+10`

## Kết Quả Train/Predict

| Horizon | Target | Feature set | Encoded feature | Dòng train | Dòng predict | MAE | RMSE | R² |
|---|---|---|---:|---:|---:|---:|---:|---:|
| t+1 | `traffic_load_t_plus_1` | `full_features` | 7 | 23,200 | 5,800 | 0.038548 | 0.048478 | 0.910143 |
| t+5 | `traffic_load_t_plus_5` | `full_features` | 7 | 23,200 | 5,800 | 0.041998 | 0.052867 | 0.892690 |
| t+10 | `traffic_load_t_plus_10` | `full_features` | 7 | 23,200 | 5,800 | 0.050441 | 0.063782 | 0.843845 |

## Horizon Diagnostics

| Horizon | MAE | RMSE | R² | MAE tăng so với t+1 | RMSE tăng so với t+1 | R² giảm so với t+1 | Quyết định |
|---|---:|---:|---:|---:|---:|---:|---|
| t+1 | 0.038548 | 0.048478 | 0.910143 | 0.000000 | 0.000000 | 0.000000 | `recommended` |
| t+5 | 0.041998 | 0.052867 | 0.892690 | 0.003450 | 0.004389 | 0.017453 | `usable` |
| t+10 | 0.050441 | 0.063782 | 0.843845 | 0.011892 | 0.015304 | 0.066298 | `usable` |

## Nhận Định

- Horizon tốt nhất theo MAE/RMSE là `t+1`.
- Horizon dài nhất còn đạt ngưỡng usable là `t+10`.
- Sai số tăng khi horizon dài hơn, nên V2 Predictive RL nên ưu tiên forecast ngắn hạn nếu chỉ cần một tín hiệu ổn định.

Figure đã tạo:

- `results/v2/horizon_analysis/figures/linear_regression_metrics_by_horizon.png`
- `results/v2/horizon_analysis/figures/linear_regression_actual_vs_prediction.png`
- `results/v2/horizon_analysis/figures/linear_regression_residual_distribution.png`
- `results/v2/horizon_analysis/figures/linear_regression_sample_timeseries.png`

## Artifact

- Report: `results/v2/horizon_analysis/README.md`
- Metric CSV: `results/v2/horizon_analysis/horizon_metrics.csv`
- Prediction CSV: `results/v2/horizon_analysis/horizon_predictions.csv`
- Figure: `results/v2/horizon_analysis/figures/`

## Kết Luận

- Forecast Horizon được đề xuất cho V2 hiện tại: `t+1`.
- Có thể chuyển sang V2 Experiment 2 - Feature Contribution Analysis.
