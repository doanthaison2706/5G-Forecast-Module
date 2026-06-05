# PROJECT OVERVIEW

## Tên dự án

 Benchmark for Predictive RL

---

# Giới thiệu

Trong đồ án chính, mục tiêu là xây dựng hệ thống Predictive Energy-aware Reinforcement Learning để tối ưu năng lượng cho trạm 5G.

Ở phiên bản V0, Agent chỉ quan sát trạng thái hiện tại của mạng và đưa ra quyết định tương ứng.

Tuy nhiên trong thực tế, việc biết trước xu hướng tải mạng có thể giúp Agent đưa ra quyết định tốt hơn thay vì chỉ phản ứng sau khi sự kiện đã xảy ra.

Vì vậy, trước khi xây dựng V2 Predictive RL, cần đánh giá khả năng dự báo tải mạng từ dữ liệu được sinh ra bởi simulator.

Dự án này được tạo ra nhằm xây dựng và đánh giá Forecast Module trước khi tích hợp vào hệ thống RL.

---

# Mục tiêu

- Xây dựng pipeline dự báo tải mạng ngắn hạn.
- Đánh giá khả năng dự báo của dữ liệu simulator.
- So sánh các mô hình dự báo khác nhau.
- Lựa chọn mô hình phù hợp để tích hợp vào V2 Predictive RL.

---

# Câu hỏi nghiên cứu

Liệu dữ liệu traffic được sinh bởi simulator có đủ khả năng dự báo để sử dụng trong Predictive RL hay không?

---

# Phạm vi dự án

## Bao gồm

- Dataset sinh từ simulator.
- Feature Engineering.
- Forecast Horizon Analysis.
- Window Size Analysis.
- So sánh mô hình dự báo.
- Đánh giá sai số dự báo.

## Không bao gồm

- Reinforcement Learning.
- PPO Training.
- Energy Optimization.
- Reward Design.
- Simulator Development.

---

# Kết quả mong đợi

- Dataset phục vụ dự báo traffic.
- Pipeline huấn luyện mô hình dự báo.
- Bộ kết quả đánh giá.
- Mô hình dự báo được chọn để sử dụng trong V2.
- Báo cáo chi tiết về quá trình xây dựng và đánh giá Forecast Module.

# Cấu trúc dự án
forecast_module_benchmark/

├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_model_benchmark.ipynb
│
├── src/
│   ├── data/
│   │   ├── dataset_loader.py
│   │   └── feature_engineering.py
│   │
│   ├── models/
│   │   ├── linear_regression.py
│   │   └── random_forest.py
│   │
│   ├── evaluation/
│   │   ├── metrics.py
│   │   └── benchmark.py
│   │
│   └── utils/
│
├── results/
│   ├── horizon_analysis.csv
│   ├── feature_analysis.csv
│   ├── model_comparison.csv
│   └── figures/
│
├── docs/
│   ├── 00_PROJECT_OVERVIEW.md
│   ├── 01_PROBLEM_STATEMENT.md
│   ├── 02_EXPERIMENT_DESIGN.md
│   └── 03_ROADMAP.md
│
├── requirements.txt
├── train.py
├── evaluate.py
└── README.md
