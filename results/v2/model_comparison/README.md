# V2 Experiment 4 - Model Comparison

Mục tiêu của thí nghiệm này là so sánh Linear Regression với Random Forest trên cùng cấu hình forecast.

## Cấu Hình Cố Định

- Target horizon: `t+1`
- Feature set: `full_features`
- Train/test split: 80/20 theo `episode_id`
- Random Forest: `n_estimators=100`, `n_jobs=1`, `random_state=42`

## Kết Quả Train/Predict

| Model | Config | Horizon | Feature set | Encoded feature | Dòng train | Dòng predict | MAE | RMSE | R² |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| `linear_regression` | `least_squares` | t+1 | `full_features` | 7 | 23,200 | 5,800 | 0.038548 | 0.048478 | 0.910143 |
| `random_forest` | `n_estimators=100, n_jobs=1, random_state=42` | t+1 | `full_features` | 7 | 23,200 | 5,800 | 0.037122 | 0.047153 | 0.914987 |

## Model Diagnostics

| Model | MAE | RMSE | R² | MAE đổi so với Linear Regression | RMSE đổi so với Linear Regression | R² tăng so với Linear Regression | Quyết định |
|---|---:|---:|---:|---:|---:|---:|---|
| `linear_regression` | 0.038548 | 0.048478 | 0.910143 | 0.000000 | 0.000000 | 0.000000 | `recommended` |
| `random_forest` | 0.037122 | 0.047153 | 0.914987 | -0.001427 | -0.001325 | 0.004844 | `recommended` |

## Nhận Định

- Model tốt nhất theo MAE/RMSE là `random_forest`.
- Random Forest được giới hạn 100 cây và chạy một worker để phù hợp máy cá nhân.
- Nếu Random Forest không cải thiện rõ rệt, Linear Regression vẫn là lựa chọn dễ giải thích và nhẹ hơn cho V2.

Figure đã tạo:

- `results/v2/model_comparison/figures/linear_regression_metrics_by_model.png`
- `results/v2/model_comparison/figures/linear_regression_actual_vs_prediction.png`
- `results/v2/model_comparison/figures/linear_regression_residual_distribution.png`
- `results/v2/model_comparison/figures/linear_regression_sample_timeseries.png`

## Artifact

- Report: `results/v2/model_comparison/README.md`
- Metric CSV: `results/v2/model_comparison/model_metrics.csv`
- Prediction CSV: `results/v2/model_comparison/model_predictions.csv`
- Figure: `results/v2/model_comparison/figures/`

## Kết Luận V2

- Model được đề xuất cho V2 hiện tại: `random_forest`.
- V2 Forecast Benchmark đã hoàn tất các experiment chính trong roadmap.
