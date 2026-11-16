# Phương Pháp Luận Và Thiết Kế Nghiên Cứu (Research Methodology Guide)

Tài liệu này cung cấp khung hướng dẫn toàn diện về phương pháp luận nghiên cứu khoa học, từ xác định câu hỏi nghiên cứu, lựa chọn phương pháp, thiết kế chọn mẫu, thu thập dữ liệu đến xử lý và biện giải kết quả cho sinh viên và học viên đại học.

---

## 1. Khung Tiếp Cận Nghiên Cứu (Research Onion Framework)

Quy trình thiết kế phương pháp nghiên cứu học thuật chuẩn bao gồm 6 lớp tiếp cận:

```text
Triết lý nghiên cứu (Thực chứng / Diễn giải)
  └── Cách tiếp cận lý thuyết (Quy nạp / Diễn dịch)
        └── Chiến lược nghiên cứu (Khảo sát / Nghiên cứu tình huống / Thực nghiệm)
              └── Lựa chọn phương pháp (Định lượng / Định tính / Hỗn hợp)
                    └── Khung thời gian (Cắt ngang - Cross-sectional / Dài hạn - Longitudinal)
                          └── Kỹ thuật thu thập & Phân tích dữ liệu
```

---

## 2. Phân Loại Phương Pháp Nghiên Cứu

### 2.1. Nghiên Cứu Định Lượng (Quantitative Research)
- **Mục tiêu**: Kiểm định giả thuyết, đo lường mối quan hệ nhân quả hoặc tương quan giữa các biến số độc lập và phụ thuộc.
- **Công cụ đo lường**: Bảng câu hỏi khảo sát cấu trúc đóng (thang đo Likert 5 mức độ hoặc 7 mức độ).
- **Quy tắc cỡ mẫu**:
  - *Công thức Yamane (1967)* (khi biết tổng thể $N$ và sai số chấp nhận $e$):
    $$n = \frac{N}{1 + N \cdot e^2}$$
  - *Quy tắc Hair et al. (2014) cho phân tích nhân tố EFA/hồi quy*: Cỡ mẫu tối thiểu gấp 5 lần số biến quan sát ($n \ge 5 \times k$), tốt nhất là gấp 10 lần ($n \ge 10 \times k$).
- **Quy trình phân tích dữ liệu**:
  1. Thống kê mô tả (Descriptive statistics): Mean, Median, Tần số, Tỷ lệ %, Độ lệch chuẩn (Std. Dev).
  2. Kiểm định độ tin cậy thang đo: Cronbach's Alpha (yêu cầu $\ge 0.70$; tương quan biến - tổng Corrected Item-Total Correlation $\ge 0.30$).
  3. Phân tích nhân tố khám phá (EFA): Hệ số KMO ($0.5 \le KMO \le 1.0$), kiểm định Bartlett ($p < 0.05$), Eigenvalue $> 1.0$, Tổng phương sai trích $\ge 50\%$.
  4. Kiểm định hồi quy / tương quan: Pearson correlation, mô hình hồi quy OLS/Logit, kiểm định hiện tượng đa cộng tuyến (VIF $< 2.0$ hoặc $< 5.0$).

### 2.2. Nghiên Cứu Định Tính (Qualitative Research)
- **Mục tiêu**: Khám phá chiều sâu bản chất của hiện tượng, lý giải cơ chế "tại sao" và "như thế nào" trong bối cảnh thực tiễn cụ thể.
- **Phương pháp thu thập**:
  - *Phỏng vấn sâu bán cấu trúc (Semi-structured in-depth interview)*: Đối tượng là chuyên gia, cán bộ quản lý hoặc người tiêu dùng mục tiêu (thường từ 8–15 đối tượng cho đến khi đạt điểm bão hòa dữ liệu - data saturation).
  - *Thảo luận nhóm tập trung (Focus Group Discussion - FGD)*: 6–8 người tham gia dưới sự điều phối của nghiên cứu viên.
  - *Nghiên cứu tình huống điển hình (Case Study)*: Phân tích một doanh nghiệp, tổ chức hoặc dự án cụ thể (áp dụng phổ biến trong báo cáo thực tập tốt nghiệp).
- **Phương pháp phân tích**: Phân tích chủ đề (Thematic Analysis), phân tích nội dung (Content Analysis), mã hóa dữ liệu (Open coding -> Axial coding -> Selective coding).

### 2.3. Nghiên Cứu Tài Liệu & Dữ Liệu Thứ Cấp (Desk Research / Secondary Data)
- Phù hợp với các đề tài tài chính, kinh tế vĩ mô, chuỗi cung ứng, kế toán kiểm toán.
- **Nguồn dữ liệu uy tín tại Việt Nam**:
  - Báo cáo tài chính kiểm toán của các doanh nghiệp niêm yết (HOSE, HNX).
  - Tổng cục Thống kê (GSO - gso.gov.vn), Ngân hàng Nhà nước (SBV - sbv.gov.vn).
  - Các tổ chức quốc tế: World Bank, ADB, IMF, OECD, UNDP.
  - Niêm giám thống kê và báo cáo thường niên chính thức.

---

## 3. Ma Trận Dữ Liệu & Bằng Chứng (Evidence Matrix)

Trước khi viết các chương phân tích, AI và sinh viên phải lập Ma trận Bằng chứng nhằm ngăn chặn nguy cơ bịa đặt số liệu:

| Biến số / Luận điểm | Nguồn thu thập | Loại dữ liệu | Kích thước / Chi tiết | Tình trạng xác minh | Vị trí sử dụng |
|---|---|---|---|---|---|
| Khả năng thanh toán hiện hành | BCTC kiểm toán 2022-2024 Cty X | Thứ cấp | Bảng CĐKT các năm | `VERIFIED` | Chương 2 (Mục 2.2.1) |
| Động lực làm việc của nhân viên | Khảo sát 150 nhân sự | Sơ cấp | Khảo sát Likert 5 | `VERIFIED` | Chương 2 (Mục 2.3) |
| Tác động của chính sách thuế mới | Báo cáo Bộ Tài chính | Thứ cấp | Quyết định số 123/QĐ-BTC | `NEEDS_VERIFICATION` | Chương 3 (Mục 3.1) |

---

## 4. Xử Lý Giới Hạn Nghiên Cứu (Research Limitations)

Mọi báo cáo học thuật chất lượng cao đều phải chỉ rõ giới hạn nghiên cứu nhằm thể hiện tính liêm chính học thuật:
- **Giới hạn không gian**: Đề tài chỉ thực hiện khảo sát tại địa bàn TP. Hồ Chí Minh / tại một doanh nghiệp cụ thể, do đó kết quả chưa thể đại diện cho toàn bộ ngành trên phạm vi cả nước.
- **Giới hạn thời gian**: Dữ liệu chỉ phản ánh giai đoạn 2021–2024, chưa đo lường tác động của các biến động chính sách kinh tế trong tương lai.
- **Giới hạn phương pháp**: Chọn mẫu thuận tiện (convenience sampling) có thể mang yếu tố thiên vị chủ quan, cần mở rộng chọn mẫu xác suất trong các nghiên cứu kế tiếp.
