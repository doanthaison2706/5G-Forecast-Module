# Benchmark Forecast Module cho Predictive RL

Dự án này xây dựng và đánh giá Forecast Module cho V2 Predictive RL. Phạm vi
hiện tại là kiểm tra và benchmark khả năng dự báo traffic từ dataset simulator.

## Trạng Thái Hiện Tại

V0 - Forecastability Check: **PASS**  
V1 - Baseline Forecast: **IN PROGRESS**

- Traffic hiện tại có tương quan cao với traffic tương lai: `t+1 = 0.9552`,
  `t+5 = 0.9428`, `t+10 = 0.9052`.
- Dataset có ba traffic regime rõ ràng: `normal`, `busy_period`, `crowd_surge`.
- Validation kỹ thuật pass 13/13 check, nên dữ liệu đủ tin cậy để modeling.
- V1 M1 Dataset Loader đã sẵn sàng để tạo train/test split 80/20 cho các horizon
  `t+1`, `t+5`, `t+10`.
- V1 M2 Feature Set Definition đã định nghĩa `traffic_only`, `traffic_ue`,
  và `full_features`.
- V1 M3 Linear Regression Baseline đã train, predict và đánh giá MAE, RMSE, R².

## Chạy Nhanh

```bash
python3 run_v0.py
python3 run_v1_m1.py
python3 run_v1_m2.py
python3 run_v1_m3.py
```

Kết quả được ghi vào:

- `data/processed/traffic_dataset_v0_clean.csv`
- `results/v0/dataset_summary.csv`
- `results/v0/validation_report.md`
- `results/v0/README.md`
- `results/v0/figures/`
- `results/v1/dataset_loader_summary.md`
- `results/v1/feature_set_definition.md`
- `results/v1/linear_regression_baseline.md`
- `results/v1/linear_regression_predictions.csv`

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

## V1 Artifact

Tạo artifact chính thức cho milestone M1:

```bash
python3 run_v1_m1.py
```

Tạo artifact chính thức cho milestone M2:

```bash
python3 run_v1_m2.py
```

Tạo artifact chính thức cho milestone M3:

```bash
python3 run_v1_m3.py
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
src/                   # Code xử lý data, validation, model
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

- `results/v1/dataset_loader_summary.md` - artifact chính thức cho M1 Dataset Loader
- `results/v1/feature_set_definition.md` - artifact chính thức cho M2 Feature Set Definition
- `results/v1/linear_regression_baseline.md` - artifact chính thức cho M3 Linear Regression Baseline
- `results/v1/linear_regression_predictions.csv` - output predict của M3

## Phạm Vi Dự Án

Dự án tập trung vào bài toán traffic forecasting cho Predictive RL. Phần train
Reinforcement Learning, reward design, energy optimization và simulator
development nằm ngoài phạm vi benchmark này.

## Bước Tiếp Theo

Hoàn thiện các phần còn lại của V1 Baseline Forecast:

- So sánh thêm theo feature set nếu cần.
- Chuẩn bị report tổng hợp V1.
- Chuyển sang V2 Forecast Benchmark sau khi baseline ổn định.
