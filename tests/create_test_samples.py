#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_test_samples.py
Tạo 2 file DOCX mẫu để kiểm thử hệ thống:
1. sample_report_valid.docx: Báo cáo học thuật chuẩn mực, đạt toàn bộ tiêu chí Phase 7.
2. sample_report_with_errors.docx: Báo cáo có chủ đích chứa các lỗi cấu trúc, trích dẫn và định dạng.
"""

import os
import sys

try:
    import docx
    from docx import Document
    from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls
    from docx.shared import Cm, Pt, RGBColor
except ImportError:
    print("Vui lòng cài đặt python-docx: pip install python-docx")
    sys.exit(1)


def add_field(p, field_text: str):
    """Chèn mã trường (Field Code) vào paragraph."""
    run = p.add_run()
    r = run._r
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> %s </w:instrText>' % (nsdecls('w'), field_text))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    r.append(fldChar1)
    r.append(instrText)
    r.append(fldChar2)
    r.append(fldChar3)


def build_valid_report(output_path: str):
    """Tạo báo cáo mẫu đạt chuẩn 100%."""
    doc = Document()
    sec = doc.sections[0]

    # Page setup
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(3.5)
    sec.right_margin = Cm(2.0)

    # Footer Page Number
    footer_p = sec.footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_p.paragraph_format.first_line_indent = Cm(0)
    add_field(footer_p, "PAGE")

    # Styles
    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(13)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.first_line_indent = Cm(1.27)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)

    h1_style = doc.styles['Heading 1']
    h1_style.font.name = 'Times New Roman'
    h1_style.font.size = Pt(16)
    h1_style.font.bold = True
    h1_style.font.color.rgb = RGBColor(0, 0, 0)
    h1_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1_style.paragraph_format.space_before = Pt(12)
    h1_style.paragraph_format.space_after = Pt(12)
    h1_style.paragraph_format.page_break_before = True
    h1_style.paragraph_format.keep_with_next = True
    h1_style.paragraph_format.first_line_indent = Cm(0)

    h2_style = doc.styles['Heading 2']
    h2_style.font.name = 'Times New Roman'
    h2_style.font.size = Pt(14)
    h2_style.font.bold = True
    h2_style.font.color.rgb = RGBColor(0, 0, 0)
    h2_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h2_style.paragraph_format.space_before = Pt(12)
    h2_style.paragraph_format.space_after = Pt(6)
    h2_style.paragraph_format.keep_with_next = True
    h2_style.paragraph_format.first_line_indent = Cm(0)

    h3_style = doc.styles['Heading 3']
    h3_style.font.name = 'Times New Roman'
    h3_style.font.size = Pt(13)
    h3_style.font.bold = True
    h3_style.font.color.rgb = RGBColor(0, 0, 0)
    h3_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h3_style.paragraph_format.space_before = Pt(6)
    h3_style.paragraph_format.space_after = Pt(6)
    h3_style.paragraph_format.keep_with_next = True
    h3_style.paragraph_format.first_line_indent = Cm(0)

    # 1. Bìa
    p_title = doc.add_paragraph("TRƯỜNG ĐẠI HỌC KINH TẾ QUỐC DÂN\nKHOA CÔNG NGHỆ THÔNG TIN", style='Normal')
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.first_line_indent = Cm(0)

    p_main = doc.add_paragraph("\n\n\nTIỂU LUẬN MÔN HỌC\nNGHIÊN CỨU CÁC NHÂN TỐ ẢNH HƯỞNG ĐẾN QUYẾT ĐỊNH SỬ DỤNG THANH TOÁN SỐ", style='Normal')
    p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_main.paragraph_format.first_line_indent = Cm(0)
    for r in p_main.runs:
        r.font.bold = True
        r.font.size = Pt(16)

    # 2. Mục lục
    doc.add_paragraph("MỤC LỤC", style='Heading 1')
    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.first_line_indent = Cm(0)
    add_field(p_toc, 'TOC \\o "1-3" \\h \\z \\u')

    # 3. Mở đầu
    doc.add_paragraph("PHẦN MỞ ĐẦU", style='Heading 1')
    doc.add_paragraph("1. Tính cấp thiết của đề tài", style='Heading 2')
    doc.add_paragraph("Trong bối cảnh nền kinh tế số phát triển mạnh mẽ, thanh toán không dùng tiền mặt đã trở thành xu thế tất yếu tại Việt Nam theo định hướng của Ngân hàng Nhà nước (Tổng cục Thống kê, 2024). Việc nghiên cứu hành vi người tiêu dùng trong lĩnh vực này đóng vai trò quan trọng trong việc thúc đẩy tài chính toàn diện.")
    
    doc.add_paragraph("2. Mục tiêu nghiên cứu", style='Heading 2')
    doc.add_paragraph("Nghiên cứu nhằm xác định các yếu tố cốt lõi tác động đến quyết định tiếp nhận công nghệ thanh toán số của giới trẻ đô thị, từ đó đề xuất hàm ý quản trị.")

    # 4. Chương 1
    doc.add_paragraph("CHƯƠNG 1. CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN NGHIÊN CỨU", style='Heading 1')
    doc.add_paragraph("1.1. Mô hình chấp nhận công nghệ TAM", style='Heading 2')
    doc.add_paragraph("Mô hình chấp nhận công nghệ TAM được đề xuất bởi Davis (1989) nhấn mạnh hai biến số nhận thức: tính hữu ích cảm nhận và tính dễ sử dụng cảm nhận. Lý thuyết này đã được kiểm chứng rộng rãi trong các nghiên cứu về hệ thống thông tin tại các quốc gia đang phát triển.")
    
    doc.add_paragraph("1.1.1. Vai trò của niềm tin và sự thuận tiện", style='Heading 3')
    doc.add_paragraph("Nhiều nghiên cứu thực nghiệm gần đây cho thấy yếu tố niềm tin đóng vai trò trung gian then chốt giữa nhận thức rủi ro và ý định sử dụng dịch vụ thanh toán trực tuyến (Nguyễn & Trần, 2023). Khách hàng có xu hướng ưu tiên các nền tảng có chính sách bảo mật minh bạch.")

    # 5. Chương 2
    doc.add_paragraph("CHƯƠNG 2. PHÂN TÍCH THỰC TRẠNG VÀ KẾT QUẢ KHẢO SÁT", style='Heading 1')
    doc.add_paragraph("2.1. Thống kê mô tả mẫu nghiên cứu", style='Heading 2')
    doc.add_paragraph("Dữ liệu khảo sát thực nghiệm thu thập từ 250 sinh viên tại khu vực TP. Hồ Chí Minh trong quý II/2025. Kết quả thống kê cơ bản được thể hiện trong bảng dưới đây:")

    # Table with caption above
    p_cap_tab = doc.add_paragraph("Bảng 2.1. Cơ cấu mẫu khảo sát theo độ tuổi và tần suất thanh toán")
    p_cap_tab.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_tab.paragraph_format.first_line_indent = Cm(0)
    for r in p_cap_tab.runs:
        r.font.bold = True

    table = doc.add_table(rows=3, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Nhóm tuổi", "Số lượng (người)", "Tỷ lệ (%)"
    r1 = table.rows[1].cells
    r1[0].text, r1[1].text, r1[2].text = "18 - 20", "145", "58.0%"
    r2 = table.rows[2].cells
    r2[0].text, r2[1].text, r2[2].text = "21 - 23", "105", "42.0%"

    p_src_tab = doc.add_paragraph("Nguồn: Kết quả xử lý dữ liệu khảo sát của tác giả (2025)")
    p_src_tab.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_src_tab.paragraph_format.first_line_indent = Cm(0)
    for r in p_src_tab.runs:
        r.font.italic = True

    doc.add_paragraph("Số liệu từ Bảng 2.1 cho thấy nhóm sinh viên năm 1 và năm 2 chiếm tỷ lệ áp đảo với mức độ tiếp cận ứng dụng ví điện tử hàng ngày rất cao.")

    # 6. Chương 3
    doc.add_paragraph("CHƯƠNG 3. GIẢI PHÁP VÀ KIẾN NGHỊ", style='Heading 1')
    doc.add_paragraph("3.1. Nhóm giải pháp nâng cao bảo mật và trải nghiệm người dùng", style='Heading 2')
    doc.add_paragraph("Dựa trên các hạn chế về lo ngại an toàn thông tin đã phát hiện ở Chương 2, các tổ chức trung gian thanh toán cần tích hợp cơ chế xác thực sinh trắc học đa lớp nhằm gia tăng niềm tin người dùng.")

    # 7. Kết luận
    doc.add_paragraph("KẾT LUẬN", style='Heading 1')
    doc.add_paragraph("Nghiên cứu đã làm rõ các nhân tố then chốt tác động đến hành vi thanh toán số. Mặc dù còn hạn chế về quy mô mẫu, đề tài đã mang lại những đóng góp thiết thực cho thực tiễn vận hành của các fintech.")

    # 8. Tài liệu tham khảo (Hanging indent APA 7)
    doc.add_paragraph("TÀI LIỆU THAM KHẢO", style='Heading 1')
    
    refs = [
        "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. MIS Quarterly, 13(3), 319–340. https://doi.org/10.2307/249008",
        "Nguyễn, V. A., & Trần, B. C. (2023). Tác động của chuyển đổi số đến hiệu quả hoạt động của ngân hàng thương mại Việt Nam. Tạp chí Kinh tế & Phát triển, 312(2), 45–56.",
        "Tổng cục Thống kê. (2024). Báo cáo tình hình kinh tế - xã hội quý IV và năm 2024. Cổng thông tin điện tử Tổng cục Thống kê."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph(ref)
        p_ref.paragraph_format.first_line_indent = Cm(-1.27)
        p_ref.paragraph_format.left_indent = Cm(1.27)
        p_ref.paragraph_format.space_after = Pt(6)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    return output_path


def build_error_report(output_path: str):
    """Tạo báo cáo có chủ đích chứa nhiều lỗi để kiểm thử khả năng bắt lỗi của scripts."""
    doc = Document()
    sec = doc.sections[0]

    # CỐ TÌNH LỖI 1: Căn lề sai (Left 2.0 thay vì 3.5cm; Top 1.5 thay vì 2.5cm)
    sec.top_margin = Cm(1.5)
    sec.bottom_margin = Cm(1.5)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(1.5)

    # CỐ TÌNH LỖI 2: Không có trường PAGE trong footer
    # (Để trống footer)

    # CỐ TÌNH LỖI 3: Dùng Font Arial 11pt, không thụt đầu dòng, giãn dòng 1.0
    normal = doc.styles['Normal']
    normal.font.name = 'Arial'
    normal.font.size = Pt(11)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    normal.paragraph_format.line_spacing = 1.0
    normal.paragraph_format.first_line_indent = Cm(0)

    # Tiêu đề sai định dạng
    doc.add_paragraph("TIỂU LUẬN CHỨA LỖI ĐỂ KIỂM THỬ")

    # CỐ TÌNH LỖI 4: Lạm dụng dòng trống liên tiếp
    doc.add_paragraph("")
    doc.add_paragraph("")
    doc.add_paragraph("")
    doc.add_paragraph("")

    # Mở đầu
    doc.add_paragraph("PHẦN MỞ ĐẦU", style='Heading 1')
    doc.add_paragraph("Đây là đoạn văn bản ngắn để kiểm thử hệ thống. Bài viết này cố tình vi phạm nhiều tiêu chuẩn.")

    # CỐ TÌNH LỖI 5: Nhảy cóc cấp độ tiêu đề: Từ Heading 1 nhảy thẳng xuống Heading 3
    h3_jump = doc.add_paragraph("1.1.1. Mục con bị nhảy cóc không qua Heading 2", style='Heading 3')
    doc.add_paragraph("Nội dung dưới mục nhảy cóc này vi phạm thứ bậc đề mục.")

    # CỐ TÌNH LỖI 6: Thứ tự chương bị nhảy (Chương 1 rồi đến Chương 3, mất Chương 2)
    doc.add_paragraph("CHƯƠNG 1. CƠ SỞ LÝ THUYẾT", style='Heading 1')
    
    # CỐ TÌNH LỖI 7: Trích dẫn mồ côi (In-text citations không hề có trong thư mục)
    doc.add_paragraph("Theo nghiên cứu của Lê Văn C (2024), các rủi ro bảo mật là rào cản lớn nhất. Ngoài ra mô hình của Smith (2025) cũng cho thấy điều tương tự.")
    
    # CỐ TÌNH LỖI 8: Nhãn nghi vấn [NEEDS_VERIFICATION]
    doc.add_paragraph("Doanh thu của công ty được ước tính tăng trưởng 85% trong năm qua [NEEDS_VERIFICATION: Chưa có báo cáo kiểm toán xác thực số liệu].")

    # Nhảy sang Chương 3
    doc.add_paragraph("CHƯƠNG 3. GIẢI PHÁP ĐỀ XUẤT", style='Heading 1')
    doc.add_paragraph("Đề xuất các giải pháp cải tiến quy trình công nghệ.")

    # CỐ TÌNH LỖI 9: THIẾU HẲN PHẦN KẾT LUẬN (Missing mandatory section)

    # Tài liệu tham khảo
    doc.add_paragraph("TÀI LIỆU THAM KHẢO", style='Heading 1')
    # CỐ TÌNH LỖI 10: Tài liệu mồ côi xuôi (Orphan reference: Vũ (2022) có trong thư mục nhưng không được trích dẫn trong bài)
    doc.add_paragraph("Vũ, D. L. (2022). Quản trị rủi ro thanh toán điện tử. NXB Tài chính.")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    return output_path


if __name__ == "__main__":
    valid_file = "C:/Users/TAN/.gemini/config/skills/academic-report-generator/tests/sample_report_valid.docx"
    error_file = "C:/Users/TAN/.gemini/config/skills/academic-report-generator/tests/sample_report_with_errors.docx"
    
    build_valid_report(valid_file)
    print(f"Đã tạo file mẫu đạt chuẩn: {valid_file}")
    
    build_error_report(error_file)
    print(f"Đã tạo file mẫu chứa lỗi: {error_file}")
