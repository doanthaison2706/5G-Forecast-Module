# V1 M5 Results Report

File này là report tổng hợp chính thức cho V1 Baseline Forecast.

## Tóm Tắt

- M1 Dataset Loader: PASS
- M2 Feature Set Definition: PASS
- M3 Linear Regression Baseline: PASS
- M4 Evaluation/Visualization: PASS
- M5 Results Report: PASS

## M1 Dataset Loader

- Tổng số dòng dataset: 29,000
- Số dòng train: 23,200
- Số dòng test: 5,800
- Tỷ lệ train/test: 80.00% / 20.00%
- Validation: PASS (13/13 check)
- Số lượng feature mặc định: 7

## M2 Feature Set

| Feature set | Raw feature | Encoded feature |
|---|---:|---:|
| `traffic_only` | 1 | 1 |
| `traffic_ue` | 2 | 2 |
| `full_features` | 5 | 7 |

- Feature set mặc định: `full_features`
- Forecast target: `t+1`, `t+5`, `t+10`

## M3 Linear Regression Baseline

| Horizon | Target | Dòng train | Dòng predict | MAE | RMSE | R² |
|---|---|---:|---:|---:|---:|---:|
| t+1 | `traffic_load_t_plus_1` | 23,200 | 5,800 | 0.038548 | 0.048478 | 0.910143 |
| t+5 | `traffic_load_t_plus_5` | 23,200 | 5,800 | 0.041998 | 0.052867 | 0.892690 |
| t+10 | `traffic_load_t_plus_10` | 23,200 | 5,800 | 0.050441 | 0.063782 | 0.843845 |

## M4 Evaluation/Visualization

| Horizon | Dòng predict | MAE | RMSE | R² | Trung bình residual | Độ lệch chuẩn residual |
|---|---:|---:|---:|---:|---:|---:|
| t+1 | 5,800 | 0.038548 | 0.048478 | 0.910143 | 0.000193 | 0.048478 |
| t+5 | 5,800 | 0.041998 | 0.052867 | 0.892690 | -0.000172 | 0.052867 |
| t+10 | 5,800 | 0.050441 | 0.063782 | 0.843845 | -0.000545 | 0.063780 |

Figure đã tạo:

- `results/v1/figures/linear_regression_metrics_by_horizon.png`
- `results/v1/figures/linear_regression_actual_vs_prediction.png`
- `results/v1/figures/linear_regression_residual_distribution.png`
- `results/v1/figures/linear_regression_sample_timeseries.png`

## Artifact

- Report tổng hợp: `results/v1/README.md`
- Metric CSV: `results/v1/linear_regression_metrics.csv`
- Prediction CSV: `results/v1/linear_regression_predictions.csv`
- Figure: `results/v1/figures/`

## Kết Luận V1

- Linear Regression là baseline hợp lệ cho forecast traffic ngắn hạn.
- Kết quả tốt nhất ở `t+1`, sau đó giảm dần ở `t+5` và `t+10`.
- V1 đủ điều kiện chuyển sang V2 Forecast Benchmark.
