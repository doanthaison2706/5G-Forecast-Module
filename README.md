# Forecast Module Benchmark for Predictive RL

Dự án này xây dựng và đánh giá Forecast Module cho V2 Predictive RL. Phạm vi
hiện tại là kiểm tra và benchmark khả năng dự báo traffic từ dataset simulator.

## Current Status

V0 - Forecastability Check: **PASS**  
V1 - Baseline Forecast: **IN PROGRESS**

- Traffic hiện tại có tương quan cao với traffic tương lai: `t+1 = 0.9552`,
  `t+5 = 0.9428`, `t+10 = 0.9052`.
- Dataset có ba traffic regimes rõ ràng: `normal`, `busy_period`, `crowd_surge`.
- Validation kỹ thuật pass 13/13 checks, nên dữ liệu đủ tin cậy để modeling.
- V1 Dataset Loader đã sẵn sàng để tạo train/test split 80/20 cho các horizon
  `t+1`, `t+5`, `t+10`.

## Quick Start

```bash
python3 run_v0.py
```

Output được ghi vào:

- `data/processed/traffic_dataset_v0_clean.csv`
- `results/v0/dataset_summary.csv`
- `results/v0/validation_report.md`
- `results/v0/README.md`
- `results/v0/figures/`

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

Tạo artifact chính thức cho milestone M1:

```bash
python3 run_v1_m1.py
```

Output:

- `results/v1/dataset_loader_summary.md`

## Project Layout

```text
data/
  raw/                 # Dataset gốc từ simulator
  processed/           # Dataset sau xử lý
docs/                  # Problem statement, roadmap, experiment design
results/
  v0/                  # Report, analysis, summary và figures của V0
  v1/                  # Artifact và report của V1
src/                   # Code xử lý data, validation, visualization
```

## Result Location

Kết quả phân tích không đặt trong `docs/` nữa. Các artifact của từng version nằm
trong `results/<version>/`.

V0 result entrypoint:

- `results/v0/README.md` - tóm tắt kết quả nghiên cứu và insight forecastability
- `results/v0/validation_report.md`
- `results/v0/dataset_summary.csv`
- `results/v0/figures/`

V1 M1 result entrypoint:

- `results/v1/dataset_loader_summary.md` - artifact chính thức cho Dataset Loader

## Project Scope

This repository focuses on traffic forecasting for Predictive RL. Reinforcement
Learning training, reward design, energy optimization, and simulator development
are outside this benchmark project.

## Next Step

Hoàn thiện V1 Baseline Forecast:

- Linear Regression training pipeline.
- MAE, RMSE, R2 cho các horizon `t+1`, `t+5`, `t+10`.
- Report kết quả vào `results/v1/`.
