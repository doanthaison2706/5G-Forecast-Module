# Problem Statement

## Bối Cảnh

Trong đồ án chính, hệ thống Reinforcement Learning được dùng để điều khiển trạm
5G theo hướng tiết kiệm năng lượng nhưng vẫn đảm bảo QoS.

Ở phiên bản V0, agent chỉ quan sát trạng thái hiện tại của mạng và đưa ra quyết
định dựa trên thông tin đang có. Cách này là Reactive Control.

## Vấn Đề

Traffic mạng thay đổi theo thời gian. Một số thời điểm có tải thấp kéo dài,
trong khi một số thời điểm xuất hiện đợt tăng tải đột ngột.

Nếu agent chỉ nhìn trạng thái hiện tại:

- Không biết traffic sắp tăng hay giảm.
- Có thể giảm công suất quá sớm.
- Có thể phản ứng chậm khi traffic tăng đột ngột.
- Dễ ảnh hưởng đến QoS.

Vì vậy cần đánh giá khả năng bổ sung forecast traffic vào quá trình ra quyết
định.

## Câu Hỏi Nghiên Cứu

Traffic được sinh bởi simulator có đủ tín hiệu để dự báo và dùng làm input cho
Predictive RL hay không?

## Giả Thuyết

Nếu traffic trong simulator có thể được dự báo với sai số chấp nhận được, forecast
traffic có thể được dùng để xây dựng Forecast State cho V2 Predictive RL.

## Mục Tiêu

### 1. Traffic Có Dự Báo Được Không?

Đánh giá khả năng dự báo của dữ liệu traffic được sinh từ simulator.

### 2. Dự Báo Được Xa Tới Đâu?

So sánh các horizon:

- `t+1`
- `t+5`
- `t+10`

### 3. Bao Nhiêu Lịch Sử Là Đủ?

So sánh các window size:

- Window = 5
- Window = 10
- Window = 20
- Window = 30

### 4. Model Nào Phù Hợp?

So sánh:

- Linear Regression
- Random Forest
- Các model mở rộng trong tương lai

## Tiêu Chí Thành Công

Dự án được xem là thành công nếu:

- Traffic của simulator có khả năng dự báo.
- Model dự báo đạt sai số ổn định.
- Xác định được Forecast Horizon phù hợp.
- Lựa chọn được một Forecast Pipeline để tích hợp vào V2 Predictive RL.
