# Tổng Quan Dự Án

## Tên Dự Án

Benchmark Forecast Module cho Predictive RL

## Giới Thiệu

Trong đồ án chính, mục tiêu là xây dựng hệ thống Predictive Energy-aware
Reinforcement Learning để tối ưu năng lượng cho trạm 5G.

Ở phiên bản V0, agent chỉ quan sát trạng thái hiện tại của mạng và đưa ra quyết
định tương ứng. Tuy nhiên trong thực tế, việc biết trước xu hướng traffic có thể
giúp agent ra quyết định tốt hơn thay vì chỉ phản ứng sau khi sự kiện đã xảy ra.

Vì vậy, trước khi xây dựng V2 Predictive RL, cần đánh giá khả năng dự báo traffic
từ dataset được sinh bởi simulator. Dự án này được tạo ra để xây dựng và đánh giá
Forecast Module trước khi tích hợp vào hệ thống RL.

## Mục Tiêu

- Xây dựng pipeline dự báo traffic ngắn hạn.
- Đánh giá khả năng dự báo của dataset simulator.
- So sánh các model dự báo khác nhau.
- Lựa chọn model phù hợp để tích hợp vào V2 Predictive RL.

## Câu Hỏi Nghiên Cứu

Dataset traffic được sinh bởi simulator có đủ tín hiệu dự báo để sử dụng trong
Predictive RL hay không?

## Phạm Vi Dự Án

### Bao Gồm

- Dataset sinh từ simulator.
- Feature Engineering.
- Forecast Horizon Analysis.
- Window Size Analysis.
- So sánh model dự báo.
- Đánh giá sai số dự báo.

### Không Bao Gồm

- Train Reinforcement Learning.
- PPO Training.
- Energy Optimization.
- Reward Design.
- Simulator Development.

## Kết Quả Mong Đợi

- Dataset phục vụ dự báo traffic.
- Pipeline train model dự báo.
- Bộ kết quả đánh giá.
- Model dự báo được chọn để sử dụng trong V2.
- Báo cáo chi tiết về quá trình xây dựng và đánh giá Forecast Module.

## Cấu Trúc Dự Án

```text
data/
  raw/                 # Dataset gốc từ simulator
  processed/           # Dataset sau xử lý
docs/                  # Tài liệu định hướng dự án
results/
  v0/                  # Artifact V0
  v1/                  # Artifact V1
src/
  data/                # Dataset Loader, Feature Set, Validation
  models/              # Model baseline và model benchmark
run_v0.py              # Chạy validation và phân tích V0
run_v1_m1.py           # Tạo artifact M1 Dataset Loader
run_v1_m2.py           # Tạo artifact M2 Feature Set Definition
run_v1_m3.py           # Tạo artifact M3 Linear Regression Baseline
```
