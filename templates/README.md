# Hướng Dẫn Sử Dụng Templates (Academic Report Templates)

Thư mục này lưu trữ các mẫu tài liệu Word (.docx), cấu trúc tham chiếu và hướng dẫn áp dụng template cho Skill `academic-report-generator`.

---

## 1. Nguyên Tắc Áp Dụng Template

Khi sinh viên hoặc người dùng bắt đầu một đề tài:
1. **Ưu tiên 1 (Highest Priority)**: File template Word chính thức do trường, khoa hoặc giảng viên cung cấp (ví dụ: `Mau_KLTN_NEU.docx`, `Template_BaoCao_UEH.docx`).
2. **Ưu tiên 2**: Văn bản quy định thể thức định dạng bằng văn bản (margins, fonts, spacing) trong đề cương môn học.
3. **Ưu tiên 3 (Default Fallback)**: Áp dụng bộ định dạng chuẩn mặc định của Skill (Quy định tại Phase 7 & `references/quality-checklist.md`).

---

## 2. Các Kiểu Mẫu Phổ Biến

### Mẫu 1: Tiểu luận môn học (Coursework Term Paper)
- Dung lượng: 15–25 trang.
- Bìa đơn giản, không cần lời cam đoan phức tạp.
- Mục lục 2–3 cấp.
- 3 chương cơ bản: Cơ sở lý thuyết -> Thực trạng -> Giải pháp.

### Mẫu 2: Khóa luận / Đồ án tốt nghiệp (Graduation Thesis)
- Dung lượng: 50–80+ trang.
- Đầy đủ Front Matter: Bìa chính, bìa phụ, trang nhận xét GVHD, lời cam đoan, lời cảm ơn, danh mục từ viết tắt, danh mục bảng, danh mục hình, mục lục.
- Cấu trúc 4–5 chương.
- Phụ lục: Bảng câu hỏi khảo sát, dữ liệu SPSS/PLS.

---

## 3. Cách Cung Cấp Mẫu Cho AI
Người dùng chỉ cần đặt file template vào thư mục làm việc hoặc gửi file cho AI kèm câu lệnh:
> "Hãy sử dụng file mẫu `Mau_Tieu_Luan.docx` này để làm định dạng chuẩn cho báo cáo của tôi."

AI sẽ phân tích các Named Styles trong file mẫu của bạn và kế thừa chính xác:
- Margins (Lề trang).
- Font chữ của Normal và Headings.
- Cấu trúc Header và Footer.
