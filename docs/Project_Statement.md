# PROBLEM STATEMENT

## Bối cảnh

Trong đồ án chính, hệ thống Reinforcement Learning được sử dụng để điều khiển trạm 5G theo hướng tiết kiệm năng lượng nhưng vẫn đảm bảo QoS.

Ở phiên bản V0, Agent chỉ quan sát trạng thái hiện tại của mạng và đưa ra quyết định dựa trên thông tin đang có.

Điều này khiến Agent hoạt động theo cơ chế phản ứng (Reactive Control).

---

# Vấn đề

Lưu lượng mạng trong thực tế luôn thay đổi theo thời gian.

Một số thời điểm có tải thấp kéo dài, trong khi một số thời điểm xuất hiện các đợt tăng tải đột ngột.

Nếu Agent chỉ nhìn trạng thái hiện tại:

- Không thể biết tải mạng sắp tăng hay giảm.
- Có thể giảm công suất quá sớm.
- Có thể phản ứng chậm khi tải tăng đột ngột.
- Dễ ảnh hưởng đến QoS.

Vì vậy cần đánh giá khả năng bổ sung thông tin dự báo vào quá trình ra quyết định.

---

# Câu hỏi nghiên cứu

Liệu traffic được sinh bởi simulator có đủ khả năng dự báo để sử dụng làm thông tin đầu vào cho Predictive RL hay không?

---

# Giả thuyết nghiên cứu

Nếu traffic trong simulator có thể được dự báo với sai số chấp nhận được, thì thông tin dự báo có thể được sử dụng để xây dựng Forecast State cho V2 Predictive RL.

---

# Mục tiêu

Dự án tập trung trả lời các câu hỏi sau:

### 1. Traffic có dự báo được hay không?

Đánh giá khả năng dự báo của dữ liệu traffic được sinh từ simulator.

### 2. Dự báo được xa tới đâu?

So sánh các mốc:

- t + 1
- t + 5
- t + 10

### 3. Bao nhiêu lịch sử là đủ?

So sánh các kích thước cửa sổ dữ liệu khác nhau.

Ví dụ:

- Window = 5
- Window = 10
- Window = 20
- Window = 30

### 4. Mô hình nào phù hợp nhất?

So sánh:

- Linear Regression
- Random Forest
- Các mô hình mở rộng trong tương lai

# Tiêu chí thành công

Dự án được xem là thành công nếu:

- Traffic của simulator có khả năng dự báo.
- Mô hình dự báo đạt sai số ổn định.
- Xác định được Forecast Horizon phù hợp.
- Lựa chọn được một Forecast Pipeline để tích hợp vào V2 Predictive RL.