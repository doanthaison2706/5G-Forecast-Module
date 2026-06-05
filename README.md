# Benchmark Forecast Module cho Predictive RL

Dự án này xây dựng và đánh giá Forecast Module cho V2 Predictive RL. Phạm vi
hiện tại là kiểm tra và benchmark khả năng dự báo traffic từ dataset simulator.

## Trạng Thái Hiện Tại

V0 - Forecastability Check: **PASS**  
V1 - Baseline Forecast: **PASS**  
V2 - Forecast Benchmark: **IN PROGRESS**

- Traffic hiện tại có tương quan cao với traffic tương lai: `t+1 = 0.9552`,
  `t+5 = 0.9428`, `t+10 = 0.9052`.
- Dataset có ba traffic regime rõ ràng: `normal`, `busy_period`, `crowd_surge`.
- Validation kỹ thuật pass 13/13 check, nên dữ liệu đủ tin cậy để modeling.
- V1 M1 Dataset Loader đã sẵn sàng để tạo train/test split 80/20 cho các horizon
  `t+1`, `t+5`, `t+10`.
- V1 M2 Feature Set Definition đã định nghĩa `traffic_only`, `traffic_ue`,
  và `full_features`.
- V1 M3 Linear Regression Baseline đã train, predict và đánh giá MAE, RMSE, R².
- V1 M4 Evaluation/Visualization đã tạo metric summary và figure đánh giá.
- V1 M5 Results Report đã gom toàn bộ kết quả V1 vào một report.
- V2 Experiment 1 Forecast Horizon Analysis đã tạo metric, diagnostic, report
  và figure riêng cho `t+1`, `t+5`, `t+10`.

## Chạy Nhanh

```bash
python3 run_v0.py
python3 run_v1.py
python3 run_v2.py
```

Kết quả được ghi vào:

- `data/processed/traffic_dataset_v0_clean.csv`
- `results/v0/dataset_summary.csv`
- `results/v0/validation_report.md`
- `results/v0/README.md`
- `results/v0/figures/`
- `results/v1/README.md`
- `results/v1/linear_regression_predictions.csv`
- `results/v1/linear_regression_metrics.csv`
- `results/v1/figures/`
- `results/v2/horizon_analysis/README.md`
- `results/v2/horizon_analysis/horizon_metrics.csv`
- `results/v2/horizon_analysis/horizon_predictions.csv`
- `results/v2/horizon_analysis/figures/`

Nếu gặp cảnh báo Matplotlib cache trên macOS, chạy:

```bash
MPLCONFIGDIR=/private/tmp/matplotlib python3 run_v0.py
```

## V1 Dataset Loader

Dataset Loader cho V1 nằm ở `src/data/dataset_loader.py`.

Chức năng hiện có:

- Load và kiểm tra các cột bắt buộc từ dataset simulator.
- Chọn target theo horizon: `1`, `5`, hoặc `10`.
- Tạo feature matrix numeric cho model baseline, bao gồm one-hot encoding cho
  `mobility_event`.
- Split train/test 80/20 theo `episode_id` mặc định để test set không trùng
  episode với train set.
- Hỗ trợ tạo dataset cho tất cả horizon bằng `build_v1_forecast_datasets`.

Ví dụ dùng nhanh:

```python
from src.data.dataset_loader import build_v1_forecast_dataset

dataset = build_v1_forecast_dataset(
    "data/processed/traffic_dataset_v0_clean.csv",
    horizon=1,
)

print(dataset.features_train.shape)
print(dataset.features_test.shape)
print(dataset.target_column)
```

## V1 Pipeline

Chạy toàn bộ V1 từ M1 đến M5:

```bash
python3 run_v1.py
```

## V2 Pipeline

Chạy V2 Experiment 1 - Forecast Horizon Analysis:

```bash
python3 run_v2.py
```

## Cấu Trúc Dự Án

```text
data/
  raw/                 # Dataset gốc từ simulator
  processed/           # Dataset sau xử lý
docs/                  # Problem statement, roadmap, experiment design
results/
  v0/                  # Report, analysis, summary và figure của V0
  v1/                  # Artifact và report của V1
  v2/                  # Artifact và report của V2 Forecast Benchmark
src/                   # Code xử lý data, validation, model, pipeline
```

## Vị Trí Kết Quả

Kết quả phân tích không đặt trong `docs/`. Artifact của từng version nằm trong
`results/<version>/`.

V0 result entrypoint:

- `results/v0/README.md` - tóm tắt kết quả nghiên cứu và insight forecastability
- `results/v0/validation_report.md`
- `results/v0/dataset_summary.csv`
- `results/v0/figures/`

V1 result entrypoint:

- `results/v1/README.md` - M5 Results Report, gom M1-M4 và kết luận V1
- `results/v1/linear_regression_metrics.csv` - output metric
- `results/v1/linear_regression_predictions.csv` - output predict
- `results/v1/figures/` - figure evaluation

V2 result entrypoint:

- `results/v2/horizon_analysis/README.md` - Experiment 1 Forecast Horizon Analysis
- `results/v2/horizon_analysis/horizon_metrics.csv` - metric và diagnostic theo horizon
- `results/v2/horizon_analysis/horizon_predictions.csv` - output predict theo horizon
- `results/v2/horizon_analysis/figures/` - figure evaluation

## Phạm Vi Dự Án

Dự án tập trung vào bài toán traffic forecasting cho Predictive RL. Phần train
Reinforcement Learning, reward design, energy optimization và simulator
development nằm ngoài phạm vi benchmark này.

## Bước Tiếp Theo

Hoàn thiện các phần còn lại của V2 Forecast Benchmark:

- Feature Contribution Analysis.
- History Window Analysis.
- Model Comparison.
