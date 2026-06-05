# V2 Experiment 2 - History Window Analysis

Mục tiêu của thí nghiệm này là đánh giá bao nhiêu bước lịch sử traffic là đủ cho dự báo.

## Cấu Hình Cố Định

- Model: `linear_regression`
- Target horizon: `t+1`
- Feature: `traffic_load` history trong cùng episode
- Window được hiểu là `lag_0` đến `lag_n`, trong đó `lag_0` là traffic hiện tại.
- Train/test split: 80/20 theo `episode_id`
- Window so sánh: `5`, `10`, `20`, `30`

## Kết Quả Train/Predict

| Window | Horizon | History feature | Dòng train | Dòng predict | MAE | RMSE | R² |
|---|---|---:|---:|---:|---:|---:|---:|
| `window_5` | t+1 | 5 | 22,800 | 5,700 | 0.032199 | 0.040528 | 0.935557 |
| `window_10` | t+1 | 10 | 22,400 | 5,600 | 0.031913 | 0.040199 | 0.934870 |
| `window_20` | t+1 | 20 | 21,600 | 5,400 | 0.031004 | 0.039044 | 0.935031 |
| `window_30` | t+1 | 30 | 20,800 | 5,200 | 0.030997 | 0.039064 | 0.931650 |

## Window Diagnostics

| Window | MAE | RMSE | R² | MAE đổi so với window 5 | RMSE đổi so với window 5 | MAE đổi so với window trước | Quyết định |
|---|---:|---:|---:|---:|---:|---:|---|
| `window_5` | 0.032199 | 0.040528 | 0.935557 | 0.000000 | 0.000000 | n/a | `recommended` |
| `window_10` | 0.031913 | 0.040199 | 0.934870 | -0.000286 | -0.000329 | -0.000286 | `recommended` |
| `window_20` | 0.031004 | 0.039044 | 0.935031 | -0.001196 | -0.001484 | -0.000910 | `recommended` |
| `window_30` | 0.030997 | 0.039064 | 0.931650 | -0.001202 | -0.001464 | -0.000006 | `recommended` |

## Nhận Định

- Window tốt nhất theo MAE/RMSE là `window_30`.
- Window gọn nhất đạt mức recommended là `window_5`.
- Nếu window dài hơn không giảm sai số rõ rệt, V2 nên dùng window ngắn hơn để giữ Forecast State nhỏ và dễ tích hợp.

Figure đã tạo:

- `results/v2/window_analysis/figures/linear_regression_metrics_by_window.png`
- `results/v2/window_analysis/figures/linear_regression_actual_vs_prediction.png`
- `results/v2/window_analysis/figures/linear_regression_residual_distribution.png`
- `results/v2/window_analysis/figures/linear_regression_sample_timeseries.png`

## Artifact

- Report: `results/v2/window_analysis/README.md`
- Metric CSV: `results/v2/window_analysis/window_metrics.csv`
- Prediction CSV: `results/v2/window_analysis/window_predictions.csv`
- Figure: `results/v2/window_analysis/figures/`

## Kết Luận

- History Window được đề xuất cho V2 hiện tại: `window_5`.
- Có thể chuyển sang V2 Experiment 3 - Feature Contribution Analysis.
