# V1 M3 Linear Regression Baseline

File này là artifact chính thức cho V1 M3 Linear Regression Baseline.

## Cấu hình

- Model: Linear Regression
- Feature set: `full_features`
- Train/test split: 80% / 20% theo `episode_id`
- Forecast target: `t+1`, `t+5`, `t+10`

## Kết Quả Output

- Train: hoàn tất cho tất cả forecast target.
- Predict: đã ghi `results/v1/linear_regression_predictions.csv`.
- Metric: MAE, RMSE, R².

## Kết quả

| Horizon | Target | Dòng train | Dòng predict | MAE | RMSE | R² |
|---|---|---:|---:|---:|---:|---:|
| t+1 | `traffic_load_t_plus_1` | 23,200 | 5,800 | 0.038548 | 0.048478 | 0.910143 |
| t+5 | `traffic_load_t_plus_5` | 23,200 | 5,800 | 0.041998 | 0.052867 | 0.892690 |
| t+10 | `traffic_load_t_plus_10` | 23,200 | 5,800 | 0.050441 | 0.063782 | 0.843845 |

## Kết luận M3

- Trạng thái train: PASS
- Trạng thái predict: PASS
- Trạng thái đánh giá metric: PASS
- Baseline này dùng làm mốc so sánh cho các cấu hình V1/V2 tiếp theo.
