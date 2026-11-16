# Tiêu Chuẩn Phản Biện Học Thuật & Đánh Giá Chất Lượng Báo Cáo (Critical Review Guide)

Tài liệu này hướng dẫn quy trình và tiêu chí phản biện học thuật độc lập (independent academic peer review), giúp AI và người học đóng vai trò một phản biện viên khắt khe, phát hiện các lỗ hổng lập luận, sai sót số liệu và mâu thuẫn nội tại trước khi nộp bài.

---

## 1. Mười Câu Hỏi Phản Biện Học Thuật Cốt Lõi (10 Critical Dimensions)

Một bài viết học thuật đạt chuẩn phải vượt qua 10 câu hỏi thẩm định sau:

| STT | Câu hỏi thẩm định học thuật | Rủi ro nếu không đạt |
|---|---|---|
| **1** | Báo cáo có trả lời trực diện và trọn vẹn câu hỏi nghiên cứu / rubric đề bài không? | Lạc đề, không đáp ứng chuẩn đầu ra của môn học. |
| **2** | Mọi luận điểm cốt lõi (Claims) có bằng chứng xác thực (Evidence) đi kèm không? | Nhận định vô căn cứ, mang tính phỏng đoán chủ quan. |
| **3** | Có kết luận nào vượt quá phạm vi dữ liệu thu thập (Overclaiming) không? | Ngụy biện khái quát hóa vội vã, kết luận không có cơ sở khoa học. |
| **4** | Có sự mâu thuẫn logic giữa các chương trong báo cáo không? | Thiếu tính nhất quán (ví dụ: Ch1 nêu 4 nhân tố, Ch2 chỉ phân tích 3, Ch3 lại đề xuất cho nhân tố thứ 5). |
| **5** | Đề tài có nhìn nhận đa chiều và đối chiếu các quan điểm trái chiều không? | Thiên vị xác nhận (Confirmation bias), thiếu chiều sâu học thuật. |
| **6** | Thiết kế phương pháp nghiên cứu và quy mô mẫu có phù hợp và khả thi không? | Sai lệch kết quả nghiên cứu, độ tin cậy thấp. |
| **7** | Báo cáo có thừa nhận trung thực các giới hạn nghiên cứu không? | Thiếu tính khiêm tốn khoa học và liêm chính học thuật. |
| **8** | Danh mục tài liệu tham khảo có trung thực, có thể kiểm chứng và không bịa đặt? | Vi phạm nghiêm trọng liêm chính học thuật (Fake citation). |
| **9** | Có hiện tượng lặp ý, câu chữ sáo rỗng hoặc độn trang (Fluff & Tautology) không? | Giảm chất lượng bài viết, gây ức chế cho người chấm. |
| **10** | Các giải pháp và kiến nghị ở Chương 3 có bắt nguồn trực tiếp từ kết quả phân tích ở Chương 2 không? | Giải pháp "trên trời", giải pháp mẫu chung chung không giải quyết vấn đề thực tế. |

---

## 2. Hệ Thống Phân Loại Mức Độ Sai Sót (Defect Severity Classification)

### 2.1. Mức Độ CRITICAL (Nghiêm Trọng — Đình Chỉ / Trừ Điểm Liêm Chính)
- **Đặc điểm**:
  - Bịa đặt số liệu khảo sát, giả mạo kết quả kiểm định mô hình.
  - Tự sinh DOI hoặc URL giả mạo không tồn tại trên thực tế.
  - Đưa ra kết luận khẳng định quan hệ nhân quả tuyệt đối mà hoàn toàn không có dữ liệu thực nghiệm.
  - Thiếu hẳn một chương hoặc phần bắt buộc theo yêu cầu đề bài.
- **Hành động bắt buộc**: Phải dừng tiến trình xuất bản tài liệu, cảnh báo đỏ và yêu cầu người dùng cung cấp dữ liệu thực hoặc viết lại luận điểm.

### 2.2. Mức Độ MAJOR (Lớn — Trừ Điểm Chuyên Môn Nặng)
- **Đặc điểm**:
  - Lập luận một chiều, thiếu bằng chứng cho các phát biểu quan trọng.
  - Mâu thuẫn giữa các phần (ví dụ: số liệu ở bảng Chương 2 không khớp với số liệu nhắc lại ở Chương 3).
  - Trích dẫn tác giả trong thân bài nhưng không có tên trong danh mục tham khảo (hoặc ngược lại).
  - Giải pháp đề xuất mang tính lý thuyết chung chung, không gắn với bất kỳ hạn chế nào đã phân tích.
- **Hành động bắt buộc**: Bổ sung luận cứ, đối soát lại danh mục trích dẫn, điều chỉnh logic giải pháp tương ứng với thực trạng.

### 2.3. Mức Độ MINOR (Nhỏ — Ảnh Hưởng Điểm Trình Bày & Điểm Cộng)
- **Đặc điểm**:
  - Sử dụng một vài từ ngữ mang tính khẩu ngữ hoặc cảm thán.
  - Thiếu dấu chấm kết thúc bảng hoặc sai nhẹ khoảng cách thụt đầu dòng.
  - Chưa chuẩn hóa ký tự ngoặc kép hoặc gạch nối Unicode.
- **Hành động**: Tự động sửa hoặc khuyến nghị người dùng điều chỉnh trong khâu format cuối cùng.

---

## 3. Mẫu Bảng Ghi Nhận Khiếm Khuyết Học Thuật (Defect Audit Log)

Khi thực hiện Phase 6, AI phải xuất bảng kiểm định học thuật chi tiết:

| Mã lỗi | Vị trí (Văn bản) | Phân loại | Mô tả bản chất khiếm khuyết | Tác động học thuật | Biện pháp khắc phục cụ thể |
|---|---|---|---|---|---|
| **DEF-01** | Mục 2.3, Đoạn 2 | `CRITICAL` | Khẳng định doanh thu tăng 50% nhờ marketing AI nhưng không trích nguồn số liệu. | Thiếu căn cứ thực nghiệm, nghi vấn số liệu ảo. | Yêu cầu bổ sung số liệu nội bộ công ty hoặc sửa thành nhận định định tính kèm hedging. |
| **DEF-02** | Mục 3.2.1, Trang 35 | `MAJOR` | Đề xuất giải pháp tăng vốn điều lệ trong khi Chương 2 chỉ phân tích văn hóa doanh nghiệp. | Giải pháp lạc đề, không xuất phát từ thực trạng. | Thay bằng giải pháp hoàn thiện quy trình truyền thông nội bộ và khen thưởng. |
| **DEF-03** | Thân bài & Thư mục | `MAJOR` | Có 3 trích dẫn `(Lê, 2024)` trong bài nhưng thư mục không có tài liệu này. | Lỗi trích dẫn mồ côi, mất điểm liêm chính. | Tra cứu và bổ sung tài liệu của Lê (2024) vào danh mục tham khảo. |
| **DEF-04** | Đoạn mở đầu Ch1 | `MINOR` | Sử dụng từ cảm thán "vô cùng bức thiết". | Văn phong chưa đủ trang trọng. | Sửa thành "mang tính cấp thiết cao trong bối cảnh...". |
