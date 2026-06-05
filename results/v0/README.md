# V0 Result Summary - Forecastability Check

## Research Question

Traffic sinh từ simulator có đủ tín hiệu để dùng cho bài toán dự báo ngắn hạn
không?

**Kết luận: Có.** Dataset đạt chất lượng kỹ thuật và có tín hiệu forecastability
rõ ở các horizon `t+1`, `t+5`, `t+10`. V0 đủ điều kiện để chuyển sang V1
Baseline Forecast.

## Main Evidence

| Evidence | Result | Meaning |
|---|---:|---|
| Corr `traffic_load` vs `t+1` | 0.9552 | Traffic rất dễ dự báo ở bước kế tiếp |
| Corr `traffic_load` vs `t+5` | 0.9428 | Tín hiệu vẫn ổn định ở horizon trung gian |
| Corr `traffic_load` vs `t+10` | 0.9052 | Horizon xa hơn khó hơn nhưng vẫn khả thi |
| Validation checks | 13/13 passed | Dataset đủ tin cậy để modeling |
| Target alignment | 0 mismatch | Các target forecast được tạo đúng |

## Traffic Pattern

Dataset có ba vùng tải rõ ràng:

| Mobility event | Count | Mean traffic_load | Range |
|---|---:|---:|---:|
| `normal` | 10,288 | 0.3927 | 0.2008 - 0.5000 |
| `busy_period` | 14,369 | 0.6391 | 0.5000 - 0.7500 |
| `crowd_surge` | 4,343 | 0.8231 | 0.7500 - 1.0000 |

Insight: traffic không chỉ dao động ngẫu nhiên mà có các regime thấp, trung bình
và cao. Điều này quan trọng cho Predictive RL vì forecast cần giúp agent nhận
biết xu hướng tăng tải trước khi QoS bị ảnh hưởng.

## Feature Insight

| Feature | Correlation with `traffic_load` | Interpretation |
|---|---:|---|
| `traffic_demand_bps` | 0.9643 | Feature mạnh nhất cho traffic hiện tại |
| `ue_count` | 0.8870 | Tín hiệu tốt, nên benchmark riêng |
| `time_ratio` | 0.3786 | Tín hiệu yếu hơn, có thể hỗ trợ pattern theo episode |

Implication: V2 nên giữ ba nhóm feature trong benchmark: Traffic Only,
Traffic + UE, và Full Features.

## Data Readiness

| Item | Value |
|---|---:|
| Rows | 29,000 |
| Episodes | 100 |
| Steps per episode | 290 |
| Missing values | 0 |
| Duplicate rows | 0 |

Validation chi tiết nằm ở `results/v0/validation_report.md`.

## Artifacts

| Artifact | Purpose |
|---|---|
| `results/v0/dataset_summary.csv` | Thống kê dataset |
| `results/v0/validation_report.md` | Báo cáo validation kỹ thuật |
| `results/v0/figures/traffic_load_distribution.png` | Phân phối traffic |
| `results/v0/figures/sample_episode_timeseries.png` | Diễn biến traffic theo thời gian |
| `results/v0/figures/traffic_load_by_mobility_event.png` | So sánh traffic theo event |

## Next Step

Triển khai V1 Baseline Forecast với Linear Regression, split 80/20, đánh giá
MAE, RMSE và R2 cho `t+1`, `t+5`, `t+10`.
