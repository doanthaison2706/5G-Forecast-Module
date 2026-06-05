# Forecast Module Benchmark for Predictive RL

Dự án này xây dựng và đánh giá Forecast Module cho V2 Predictive RL. Phạm vi
hiện tại là kiểm tra và benchmark khả năng dự báo traffic từ dataset simulator.

## Current Status

V0 - Forecastability Check: **PASS**

- Traffic hiện tại có tương quan cao với traffic tương lai: `t+1 = 0.9552`,
  `t+5 = 0.9428`, `t+10 = 0.9052`.
- Dataset có ba traffic regimes rõ ràng: `normal`, `busy_period`, `crowd_surge`.
- Validation kỹ thuật pass 13/13 checks, nên dữ liệu đủ tin cậy để modeling.

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

## Project Layout

```text
data/
  raw/                 # Dataset gốc từ simulator
  processed/           # Dataset sau xử lý
docs/                  # Problem statement, roadmap, experiment design
results/
  v0/                  # Report, analysis, summary và figures của V0
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

## Project Scope

This repository focuses on traffic forecasting for Predictive RL. Reinforcement
Learning training, reward design, energy optimization, and simulator development
are outside this benchmark project.

## Next Step

V1 sẽ xây dựng baseline Linear Regression với train/test split 80/20 và đánh giá
MAE, RMSE, R2 cho các horizon `t+1`, `t+5`, `t+10`.
