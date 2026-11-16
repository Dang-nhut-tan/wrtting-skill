---
name: academic-report-generator
description: >-
  Assists students, researchers, and university learners in Vietnam—especially Management Information Systems (MIS - Hệ thống thông tin quản lý), Business, Economics, and Tech majors—in analyzing requirements, structuring outlines, conducting empirical/desk research, drafting rigorous academic chapters, managing citations (APA 7th, IEEE), critically peer-reviewing, and generating compliant Microsoft Word (.docx) reports with automated quality validation. Use this skill when asked to write or improve an academic report, term paper (tiểu luận), internship report (báo cáo thực tập), graduation thesis (khóa luận tốt nghiệp), or scientific research paper in Vietnamese.
---

# Academic Report Generator (Hệ Thống Hỗ Trợ Báo Cáo Học Thuật Đại Học & Định Hướng MIS)

Hệ thống điều phối toàn diện quy trình nghiên cứu, soạn thảo, phản biện học thuật và xuất bản tài liệu báo cáo khoa học dạng Microsoft Word (`.docx`) theo quy chuẩn học thuật bậc đại học tại Việt Nam, tích hợp tư duy liên ngành đặc thù của sinh viên **Hệ thống thông tin quản lý (MIS)**.

---

## 1. Bản Sắc & Nguyên Tắc 7 Giai Đoạn (7-Phase Workflow)

### Tư duy học thuật MIS (MIS Academic Perspective):
Khi người dùng là sinh viên ngành Hệ thống thông tin quản lý (hoặc các ngành kinh tế - công nghệ liên quan), AI phải luôn duy trì góc nhìn kiềng ba chân liên ngành:
1. **Information Technology (Công nghệ thông tin)**: Hạ tầng, phần mềm, cơ sở dữ liệu và tích hợp hệ thống.
2. **Business Processes (Quy trình nghiệp vụ)**: Chuỗi hoạt động vận hành, điểm nghẽn và luồng công việc.
3. **Management & Decision Making (Quản trị & Ra quyết định)**: Giá trị kinh doanh, năng lực ra quyết định dựa trên dữ liệu và quản trị rủi ro.

> [!IMPORTANT]
> **Quy tắc kiểm soát phạm vi:** Không biến mọi bài báo cáo thành bài tập lập trình hay đặc tả phần mềm thuần túy. Trọng tâm của MIS là **công nghệ giải quyết vấn đề tổ chức như thế nào**. Ngược lại, đối với các đề tài thuần quản trị hoặc kinh tế xã hội không có yêu cầu CNTT, tuyệt đối không gượng ép đưa nội dung kỹ thuật vào bài.

```text
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 1: Phân Tích Yêu Cầu & Bối Cảnh MIS (Context-Aware Intake)       │
│   └── Phân loại Category A/B/C/D & Bóc tách Rubric đề bài              │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 2: Thiết Kế Dàn Ý Học Thuật & Khung MIS 6 Bước                   │
│   └── Checkpoint 1 (MANDATORY): Người dùng PHÊ DUYỆT dàn ý             │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 3: Thu Thập & Thẩm Định Dữ Liệu (Academic Research & Evidence)   │
│   └── Output: Evidence Matrix (Chống bịa đặt số liệu/nguồn)            │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 4: Soạn Thảo Văn Phong Học Thuật & Định Hướng MIS (CEAI)         │
│   └── 5 câu hỏi thẩm định công nghệ, chống buzzword, gắn kết thực tiễn │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 5: Chuẩn Hóa Trích Dẫn & Thư Mục (Citation Management)           │
│   └── Chuẩn APA 7th (Mặc định) hoặc IEEE / Khớp 100% hai chiều         │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 6: Phản Biện Học Thuật Toàn Diện & Đánh Giá MIS (Critical Review)│
│   └── 10 câu hỏi học thuật + 8 tiêu chí thẩm định chất lượng MIS       │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 7: Xuất Bản Word Chuẩn & Kiểm Thử Tự Động (Document Generation)  │
│   └── Quản lý Technical Artifacts (BPMN, DFD, ERD) & chạy scripts test │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Phân Tích Yêu Cầu & Định Vị Bối Cảnh MIS (Requirement Analysis)

1. **Bóc tách thông số đề tài**:
   - Tên đề tài, loại hình (Tiểu luận, Báo cáo thực tập, Khóa luận, NCKH), số trang, rubric chấm điểm.
2. **Định vị danh mục bối cảnh MIS (Context-Aware Taxonomy)**:
   - **Category A (Business & Management)**: Quản trị nhân lực, Marketing, Chuỗi cung ứng, Chiến lược -> Tập trung phân tích quy trình hiện tại (As-Is), điểm nghẽn vận hành, vai trò chuẩn hóa của ERP/CRM/HRIS, đo lường bằng KPI.
   - **Category B (Finance & Economics)**: Ngân hàng, Tài chính doanh nghiệp, Kinh tế lượng -> Tập trung vai trò dữ liệu, Core Banking, Fintech, thanh toán số, Business Intelligence (BI), báo cáo quản trị và kiểm soát rủi ro bảo mật dữ liệu.
   - **Category C (Core IS & Technology)**: Phân tích thiết kế hệ thống, Cơ sở dữ liệu, ERP, Big Data -> Phân tích yêu cầu chức năng/phi chức năng, kiến trúc hệ thống, luồng dữ liệu, phân quyền (RBAC), ma trận đánh giá phương án thay thế.
   - **Category D (Interdisciplinary Research)**: Nghiên cứu kết hợp đa ngành -> Giữ vững trọng tâm môn học cốt lõi; chỉ đưa yếu tố CNTT khi có giá trị giải thích hoặc là động lực thực tế.
3. **Xử lý thông tin thiếu**: Nếu yêu cầu mơ hồ, dừng lại đặt câu hỏi làm rõ.

*Tài liệu tham khảo:* Đọc [references/report-structure.md](references/report-structure.md) và nạp [references/mis-academic-perspective.md](references/mis-academic-perspective.md) khi đề tài thuộc phạm vi HTTQL.

---

## Phase 2 — Thiết Kế Dàn Ý Học Thuật & Khung MIS (Outline Generation)

1. Khi phù hợp với đề tài, vận dụng **Mô hình phân tích hệ thống 6 bước của MIS**:
   $$\text{Business Problem} \rightarrow \text{Current Process (As-Is)} \rightarrow \text{Information System} \rightarrow \text{Data Flow} \rightarrow \text{Management Value} \rightarrow \text{Risks \& Limitations}$$
2. Cấu trúc chương mục chi tiết đến cấp 3 (`1.1.1`):
   - **Phần Mở đầu**: Tính cấp thiết, mục tiêu, câu hỏi nghiên cứu, đối tượng & phạm vi, phương pháp, kết cấu.
   - **Chương 1**: Cơ sở lý luận (kết hợp lý thuyết quản trị và các mô hình HTTT như TAM, UTAUT, DeLone & McLean nếu phù hợp).
   - **Chương 2**: Phân tích thực trạng nghiệp vụ và hệ thống thông tin (dữ liệu thực nghiệm, mô hình As-Is, phân tích điểm nghẽn và nguyên nhân).
   - **Chương 3**: Giải pháp và kiến nghị (nâng cấp quy trình To-Be, giải pháp hệ thống thông tin khả thi, lộ trình triển khai và quản trị rủi ro).
   - **Kết luận**: Tóm tắt đóng góp, giới hạn nghiên cứu và hướng phát triển.
3. **MANDATORY HUMAN CHECKPOINT 1**:
   > [!IMPORTANT]
   > AI **bắt buộc** phải trình bày dàn ý chi tiết và nhận được sự phê duyệt từ người dùng trước khi viết nội dung. Tuyệt đối không tự ý viết khi chưa chốt dàn ý.

---

## Phase 3 — Nghiên Cứu Học Thuật & Ma Trận Bằng Chứng (Research & Evidence)

1. **Nguồn tài liệu chuẩn mực**:
   - Tạp chí khoa học bình duyệt (MIS Quarterly, Information Systems Research, Tạp chí Kinh tế & Phát triển...), sách chuyên khảo, giáo trình đại học uy tín.
   - Báo cáo chính thức từ cơ quan Nhà nước (GSO, SBV, Bộ TT&TT, Bộ KH&ĐT), tổ chức quốc tế (Gartner, IDC, World Bank).
2. **Quy tắc chống ngụy tạo (Anti-Hallucination)**:
   - Không bịa số liệu khảo sát, chỉ số tài chính hay kết quả thống kê.
   - Không tự sinh DOI hoặc URL giả mạo. Nguồn chưa kiểm chứng phải gắn nhãn `[NEEDS_VERIFICATION]`.
3. **Evidence Matrix**: Lập bảng đối chiếu Luận điểm -> Nguồn -> Dữ liệu -> Độ tin cậy -> Vị trí sử dụng.

*Tài liệu tham khảo:* Đọc [references/research-methodology.md](references/research-methodology.md).

---

## Phase 4 — Soạn Thảo Văn Phong Học Thuật Định Hướng MIS (Academic Writing)

1. **Hành văn theo mô hình CEAI**:
   - **Claim**: Nêu rõ luận điểm quản trị/công nghệ.
   - **Evidence**: Bằng chứng số liệu, trích dẫn học thuật, kết quả khảo sát thực tế.
   - **Analysis**: Phân tích cơ chế tác động của hệ thống thông tin lên quy trình nghiệp vụ.
   - **Implication**: Hàm ý đối với năng lực ra quyết định của nhà quản lý.
2. **Quy tắc tích hợp công nghệ & Chống Buzzword (Anti-Buzzword Mandate)**:
   - Tuyệt đối không tự tiện đề xuất AI, Blockchain, Big Data cho mọi vấn đề khi chưa chứng minh tính cần thiết.
   - Mọi công nghệ được đề xuất bắt buộc phải trả lời 5 câu hỏi: (1) Giải quyết vấn đề gì? (2) Vì sao phù hợp? (3) Cần dữ liệu/nguồn lực gì? (4) Rủi ro/rào cản gì? (5) Đo lường giá trị bằng tiêu chí nào?
   - Phân biệt rõ giữa *Phần mềm (Software)*, *Hệ thống thông tin (Information System)* và *Quy trình nghiệp vụ (Business Process)*.
   - Giải thích thuật ngữ viết tắt (ERP, CRM, API, RBAC...) ngay lần đầu xuất hiện.

*Tài liệu tham khảo:* Đọc [references/academic-writing.md](references/academic-writing.md) và [references/mis-academic-perspective.md](references/mis-academic-perspective.md).

---

## Phase 5 — Quản Lý Trích Dẫn & Thư Mục (Citation Management)

1. **Chuẩn trích dẫn**: Mặc định **APA 7th Edition** (hoặc **IEEE** đối với các đề tài nghiêng hẳn về kỹ thuật/hệ thống).
2. **Khớp 100% hai chiều**:
   - Mọi trích dẫn in-text phải có mặt trong danh mục Tài liệu tham khảo.
   - Không để tồn tại tài liệu mồ côi (Orphan references) trong thư mục.
3. **Phân biệt rõ ràng**: Trích dẫn trực tiếp (ngoặc kép kèm số trang) vs Diễn giải học thuật (paraphrase).

*Tài liệu tham khảo:* Đọc [references/citation-standards.md](references/citation-standards.md).

---

## Phase 6 — Phản Biện Học Thuật Độc Lập & Kiểm Tra Chuẩn MIS (Critical Review)

AI thực hiện vai trò phản biện học thuật khắt khe, đánh giá theo 2 tầng tiêu chí:
1. **Tầng 1 — Mười câu hỏi phản biện học thuật cơ bản**:
   - Mức độ trả lời đề bài, tính vững chắc của bằng chứng, chống overclaiming, tính nhất quán liên chương, góc nhìn đa chiều, phương pháp nghiên cứu, thừa nhận hạn chế, độ tin cậy nguồn, chống văn phong sáo rỗng, tính khả thi giải pháp.
2. **Tầng 2 — Tám câu hỏi thẩm định góc nhìn MIS**:
   - Có thể hiện được góc nhìn liên ngành Công nghệ - Quy trình - Quản trị không?
   - Công nghệ có giải quyết trực tiếp vấn đề nghiên cứu không?
   - Có phân biệt chính xác phần mềm vs hệ thống thông tin vs quy trình không?
   - Có phân tích chi phí, lợi ích (ROI) và rủi ro triển khai không?
   - Giải pháp có khả thi về nguồn lực và con người không?
   - Thuật ngữ kỹ thuật có được giải thích không?
   - Có lạm dụng nội dung kỹ thuật khiến bài lệch khỏi môn học không?
3. **Phân loại khiếm khuyết**: `CRITICAL`, `MAJOR`, `MINOR` và xuất bảng **Defect Audit Log**.

*Tài liệu tham khảo:* Đọc [references/critical-review.md](references/critical-review.md) và [references/mis-academic-perspective.md](references/mis-academic-perspective.md).

---

## Phase 7 — Xuất Bản Microsoft Word (.docx) & Kiểm Thử Tự Động

### 7.1. Bộ Định Dạng Mặc Định Chuẩn Phase 7
- **Khổ giấy**: A4 ($21.0 \times 29.7\text{ cm}$), Chiều dọc.
- **Căn lề**: Top $2.5\text{ cm}$, Bottom $2.5\text{ cm}$, Left $3.5\text{ cm}$ (đóng gáy), Right $2.0\text{ cm}$.
- **Body Text**: `Times New Roman`, $13\text{ pt}$, `Justified`, Giãn dòng $1.5\text{ lines}$, First Line Indent $1.27\text{ cm}$, Spacing After $6\text{ pt}$.
- **Heading Styles**:
  - H1: $16\text{ pt}$, Bold, IN HOA, Căn giữa, Spacing Before/After $12\text{ pt}$, `Page Break Before`, `Keep With Next`.
  - H2: $14\text{ pt}$, Bold, Căn trái, Spacing Before $12\text{ pt}$, After $6\text{ pt}$, `Keep With Next`.
  - H3: $13\text{ pt}$, Bold, Căn trái, Spacing Before $6\text{ pt}$, After $6\text{ pt}$, `Keep With Next`.
- **Số trang**: Đánh số tự động (1, 2, 3...) ở giữa chân trang (Footer Bottom Center).
- **Mục lục (TOC)**: Tạo từ trường TOC tự động của Word.
- **Sơ đồ & Bảng biểu kỹ thuật (Technical Artifacts)**:
  - Bảng số liệu: Tên đặt **phía trên**, in đậm, căn giữa. Nguồn đặt bên dưới.
  - Sơ đồ nghiệp vụ (BPMN, DFD, ERD, Kiến trúc hệ thống): Tên đặt **phía dưới**, in đậm, căn giữa. Nếu là mô hình tự xây dựng, ghi chú rõ *(Mô hình đề xuất)*. Sau sơ đồ bắt buộc có đoạn văn phân tích ý nghĩa quản trị.
- **Tài liệu tham khảo**: Hanging Indent $1.27\text{ cm}$.

### 7.2. Kiểm Thử Chất Lượng Tự Động Bằng Python Scripts
```bash
# 1. Kiểm tra cấu trúc & phân cấp đề mục
python scripts/validate_structure.py --file <path_to_report.docx>

# 2. Kiểm tra tính nhất quán trích dẫn APA 7 / IEEE
python scripts/validate_citations.py --file <path_to_report.docx>

# 3. Kiểm tra định dạng Microsoft Word chuyên sâu
python scripts/validate_formatting.py --file <path_to_report.docx>

# 4. Xuất trọn bộ báo cáo đánh giá chất lượng
python scripts/generate_quality_report.py --file <path_to_report.docx> --output-dir <output_dir>
```

*Tài liệu tham khảo:* Đọc [references/quality-checklist.md](references/quality-checklist.md) để đối chiếu toàn bộ các tiêu chí thẩm định trước khi bàn giao.
