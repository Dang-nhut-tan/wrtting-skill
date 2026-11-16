# Academic Report Generator — Antigravity Skill (Định Hướng MIS & Đa Ngành)

**Academic Report Generator** là Skill toàn diện dành cho Google Antigravity, được thiết kế chuyên biệt để hỗ trợ sinh viên ngành **Hệ thống thông tin quản lý (Management Information Systems — MIS)**, các khối ngành Kinh tế, Quản trị và Công nghệ tại Việt Nam xây dựng báo cáo khoa học, tiểu luận môn học, báo cáo thực tập và khóa luận tốt nghiệp đạt chuẩn học thuật và chuẩn định dạng Microsoft Word (`.docx`).

---

## 1. Nghiên Cứu & Kiến Trúc Customization Trong Google Antigravity

Dựa trên tài liệu chính thức của hệ thống Antigravity Customization (`agy-customizations`), hệ thống phân định rõ 3 loại cấu hình:

| Thành phần | Đường dẫn định nghĩa | Cơ chế tải (Loading) | Mục đích sử dụng cốt lõi |
|---|---|---|---|
| **Rules** | `GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md` | Tải ngữ cảnh tự động (Always-on hoặc theo mẫu file) | Ràng buộc hành vi code, quy ước ngôn ngữ, đạo đức và ranh giới an toàn. |
| **Skills** | `skills/<name>/SKILL.md` (Global: `~/.gemini/config/skills/`, Project: `.agents/skills/`) | Tải theo nhu cầu (**Progressive Disclosure** qua `name` & `description`) | Cung cấp tri thức chuyên sâu, quy trình nhiều bước, tài liệu tham khảo và script thực thi. |
| **Workflows** | `run_workflow` (Python script điều phối đa tác tử) | Thực thi theo luồng tác tử chuyên biệt | Fan-out song song, tổng hợp kết quả giữa các tác tử độc lập. *(Các workflow YAML cũ đã được di chuyển sang Skills)*. |

### Vị Trí Cài Đặt Của Skill
- **Cấu hình Toàn cục (Global - Mọi dự án đều dùng được):**
  `C:\Users\<USER>\.gemini\config\skills\academic-report-generator\`
- **Cấu hình Dự án (Project-specific):**
  `<Project_Root>\.agents\skills\academic-report-generator\`

---

## 2. Cấu Trúc Thư Mục Skill

```text
academic-report-generator/
├── SKILL.md                          # Tệp điều phối chính (Orchestrator & Frontmatter)
├── references/                       # Tài liệu tham khảo chuyên sâu (Progressive Disclosure)
│   ├── mis-academic-perspective.md   # [MỚI] Góc nhìn học thuật MIS: Phân loại đề tài, chuỗi 6 bước, 5 câu hỏi thẩm định công nghệ
│   ├── academic-writing.md           # Văn phong học thuật tiếng Việt, mô hình CEAI, chống ngụy biện
│   ├── research-methodology.md       # Phương pháp nghiên cứu định lượng/định tính, cỡ mẫu, ma trận bằng chứng
│   ├── citation-standards.md         # Quy chuẩn trích dẫn APA 7th Edition, IEEE & quy định ĐH Việt Nam
│   ├── report-structure.md           # Cấu trúc giải phẫu báo cáo, tiểu luận, KLTN từ bìa đến phụ lục
│   ├── critical-review.md            # Tiêu chuẩn phản biện học thuật 10 chiều, phân loại lỗi CRITICAL/MAJOR/MINOR
│   └── quality-checklist.md          # Bảng kiểm tra chất lượng 50+ tiêu chí toàn diện
├── templates/                        # Quản lý mẫu tài liệu Word (.docx)
│   ├── README.md                     # Hướng dẫn tích hợp template riêng của trường/khoa
│   ├── academic_template_generator.py # Script sinh template Word chuẩn Phase 7
│   └── Academic_Report_Template.docx # File mẫu Word chuẩn sạch sẵn sàng sử dụng
├── scripts/                          # Bộ công cụ kiểm thử chất lượng tự động bằng Python
│   ├── validate_structure.py         # Kiểm tra cấu trúc phần bắt buộc, thứ tự chương, heading hierarchy
│   ├── validate_citations.py         # Kiểm tra khớp 100% hai chiều trích dẫn in-text và thư mục APA/IEEE
│   ├── validate_formatting.py        # Kiểm tra khổ giấy A4, margins, font 13pt Times New Roman, 1.5 lines, TOC, PAGE
│   └── generate_quality_report.py    # Điều phối và xuất Formatting_Validation.md & Academic_Quality_Report.md
├── tests/                            # Bộ kiểm thử tự động (Unit Tests & Sample Fixtures)
│   ├── sample_report_valid.docx      # File mẫu kiểm thử đạt chuẩn
│   ├── sample_report_with_errors.docx# File mẫu kiểm thử chứa lỗi chủ đích
│   ├── create_test_samples.py        # Script sinh 2 file mẫu kiểm thử
│   ├── test_validators.py            # Test suite tự động cho các validators (7/7 pass)
│   └── test_mis_perspectives.py      # [MỚI] Test suite kiểm thử phân loại đề tài & chống buzzword MIS (5/5 pass)
└── README.md                         # Hướng dẫn cài đặt, kích hoạt và sử dụng Skill
```

---

## 3. Đặc Trưng Học Thuật Chuyên Biệt Dành Cho Sinh Viên MIS

Khi người dùng là sinh viên Hệ thống thông tin quản lý (MIS), hệ thống kích hoạt **MIS Academic Perspective**:

### 3.1. Bản Sắc Kiềng Ba Chân (The MIS Triad)
- **Information Technology**: Công nghệ, phần mềm, cơ sở dữ liệu, API, Cloud.
- **Business Processes**: Quy trình tác nghiệp hiện tại (As-Is), điểm nghẽn, quy trình tương lai (To-Be).
- **Management & Decision Making**: Giá trị quản trị, hỗ trợ ra quyết định dựa trên dữ liệu, quản trị rủi ro.

### 3.2. Bốn Nhóm Bối Cảnh Đề Tài (Context-Aware Taxonomy)
1. **Category A — Quản trị & Kinh doanh (Business & Management)**: Quản trị nhân lực, Marketing, Chuỗi cung ứng -> Phân tích điểm nghẽn quy trình, chuẩn hóa bằng ERP/CRM/HRIS, đo lường KPI.
2. **Category B — Tài chính & Kinh tế (Finance & Economics)**: Ngân hàng, Tài chính doanh nghiệp, Kinh tế lượng -> Dữ liệu tài chính, Core Banking, Fintech, thanh toán số, Business Intelligence (BI), báo cáo quản trị và bảo mật.
3. **Category C — Hệ thống & Công nghệ cốt lõi (IS & Technology)**: Phân tích thiết kế hệ thống, CSDL, Big Data -> Phân tích yêu cầu chức năng/phi chức năng, kiến trúc phân tầng, mô hình ERD, kiểm soát phân quyền (RBAC), ma trận đánh giá phương án thay thế.
4. **Category D — Nghiên cứu liên ngành**: Giữ vững trọng tâm môn học, chỉ đưa yếu tố công nghệ khi thực sự có giá trị phân tích thực tiễn.

### 3.3. Khung Phân Tích Hệ Thống 6 Bước
$$\text{Business Problem} \rightarrow \text{Current Process (As-Is)} \rightarrow \text{Information System} \rightarrow \text{Data Flow} \rightarrow \text{Management Value} \rightarrow \text{Risks \& Limitations}$$

### 3.4. Năm Câu Hỏi Thẩm Định Công Nghệ Bắt Buộc (Anti-Buzzword Mandate)
Tuyệt đối không tự tiện đề xuất AI, Blockchain, Big Data cho mọi đề tài. Mỗi công nghệ đề cập phải giải trình:
1. Giải quyết vấn đề nghiệp vụ nào?
2. Vì sao phù hợp với tổ chức/đề tài?
3. Cần dữ liệu và nguồn lực nào?
4. Có những rủi ro và rào cản triển khai gì?
5. Giá trị mang lại được đánh giá bằng chỉ số nào?

---

## 4. Yêu Cầu Môi Trường & Cài Đặt

### 4.1. Yêu Cầu Kỹ Thuật
- **Python**: Phiên bản 3.10 trở lên.
- **Thư viện bắt buộc**: `python-docx` (phiên bản 1.0 trở lên).

### 4.2. Cài Đặt Dependencies
Mở Terminal/PowerShell và chạy lệnh:
```bash
pip install python-docx
```

Kiểm tra cài đặt:
```bash
python -c "import docx; print('python-docx version:', docx.__version__)"
```

---

## 5. Cách Kích Hoạt Skill Bằng Tiếng Việt (Prompt Examples)

### Ví Dụ 1: Bắt đầu viết tiểu luận MIS / Quản trị
> *"Tôi là sinh viên ngành HTTQL đang làm tiểu luận môn Quản trị Nhân sự với đề tài 'Nghiên cứu ứng dụng hệ thống HRIS nhằm chuẩn hóa quy trình đánh giá hiệu suất nhân viên tại doanh nghiệp bán lẻ'. Hãy áp dụng skill academic-report-generator để phân loại đề tài, bóc tách rubric và xây dựng dàn ý theo khung 6 bước MIS."*

### Ví Dụ 2: Đề tài Tài chính - Ngân hàng
> *"Tôi cần làm báo cáo môn Ngân hàng Thương mại về đề tài 'Đánh giá rủi ro an ninh dữ liệu trong triển khai ứng dụng Ngân hàng số (Digital Banking)'. Hãy lên dàn ý chi tiết tích hợp góc nhìn hệ thống thông tin tài chính Category B."*

### Ví Dụ 3: Đề tài Phân tích thiết kế hệ thống (Category C)
> *"Tôi cần làm đồ án môn Phân tích Thiết kế Hệ thống Thông tin đề tài 'Hệ thống Quản lý Khách sạn trực tuyến'. Hãy xây dựng dàn ý chi tiết gồm sơ đồ Use Case, DFD, ERD và ma trận so sánh kiến trúc Microservices vs Monolith."*

### Ví Dụ 4: Chạy kiểm thử tự động toàn diện
> *"Hãy kiểm tra toàn bộ file báo cáo `BaoCao_MIS.docx` về cấu trúc đề mục, trích dẫn APA và định dạng Microsoft Word."*

---

## 6. Hướng Dẫn Sử Dụng Bộ Scripts Kiểm Thử Độc Lập

```bash
# 1. Kiểm tra cấu trúc & đề mục
python scripts/validate_structure.py --file "duong_dan/BaoCao.docx"

# 2. Kiểm tra trích dẫn (APA 7th / IEEE)
python scripts/validate_citations.py --file "duong_dan/BaoCao.docx"

# 3. Kiểm tra định dạng Word (.docx)
python scripts/validate_formatting.py --file "duong_dan/BaoCao.docx"

# 4. Tổng hợp báo cáo chất lượng toàn diện (All-in-One)
python scripts/generate_quality_report.py --file "duong_dan/BaoCao.docx" --output-dir "output/"

# 5. Chạy toàn bộ Test Suites của Skill
python tests/test_validators.py
python tests/test_mis_perspectives.py
```

---

## 7. Các Giới Hạn Kiểm Định & Hướng Dẫn Thao Tác Thủ Công

1. **Cập nhật Mục lục trong Word (TOC Field)**:
   - `python-docx` không render bố cục trang in. Sau khi sinh file, mở file trên Microsoft Word, bấm **`Ctrl + A` -> `F9`** (hoặc chuột phải vào Mục lục -> *Update Field* -> *Update entire table*) để cập nhật số trang chuẩn xác.
2. **Xác minh nguồn tài liệu ngoài đời thực**:
   - `validate_citations.py` kiểm tra **tính nhất quán văn bản nội tại** (khớp 100% giữa in-text và thư mục). Để kiểm tra sự tồn tại ngoài đời thực của bài báo, người học cần đối soát DOI hoặc tra cứu trên Google Scholar/Scopus đối với các mục bị gắn nhãn `[NEEDS_VERIFICATION]`.
3. **Quy chuẩn ưu tiên mẫu của trường**:
   - Bộ định dạng mặc định (A4, lề 2.5-2.5-3.5-2.0cm, 13pt Times New Roman, 1.5 lines) là thiết lập tối ưu của Skill. Nếu trường hoặc khoa cung cấp file template Word riêng, **luôn ưu tiên mẫu của trường**.
