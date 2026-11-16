#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
academic_template_generator.py
Trình tạo tài liệu và template Microsoft Word (.docx) chuẩn học thuật Việt Nam theo Phase 7.

Thiết lập chuẩn:
- Khổ giấy A4 (21 x 29.7 cm)
- Căn lề: Top 2.5cm, Bottom 2.5cm, Left 3.5cm, Right 2.0cm
- Normal: Times New Roman 13pt, Justified, 1.5 lines, First-line indent 1.27cm, Space after 6pt
- Heading 1: 16pt Bold In hoa Căn giữa, Spacing before/after 12pt, Page Break Before, Keep With Next
- Heading 2: 14pt Bold Căn trái, Spacing before 12pt, after 6pt, Keep With Next
- Heading 3: 13pt Bold Căn trái, Spacing before 6pt, after 6pt, Keep With Next
- Footer: Số trang tự động (PAGE field) ở giữa chân trang
- TOC: Trường mã TOC tự động
"""

import os
import sys
from typing import Optional

try:
    import docx
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement, parse_xml
    from docx.oxml.ns import nsdecls, qn
    from docx.shared import Cm, Inches, Pt, RGBColor
except ImportError:
    print("Vui lòng cài đặt python-docx: pip install python-docx")
    sys.exit(1)


def add_field(p, field_text: str):
    """Thêm một mã trường Word (Field code như PAGE, TOC) vào paragraph."""
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


def setup_document_styles(doc: Document):
    """Cấu hình các Named Styles theo chuẩn định dạng Phase 7."""
    styles = doc.styles

    # 1. Normal Style
    normal = styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(13)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.first_line_indent = Cm(1.27)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)

    # 2. Heading 1
    h1 = styles['Heading 1']
    h1.font.name = 'Times New Roman'
    h1.font.size = Pt(16)
    h1.font.bold = True
    h1.font.color.rgb = RGBColor(0, 0, 0)
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(12)
    h1.paragraph_format.page_break_before = True
    h1.paragraph_format.keep_with_next = True
    h1.paragraph_format.first_line_indent = Cm(0)

    # 3. Heading 2
    h2 = styles['Heading 2']
    h2.font.name = 'Times New Roman'
    h2.font.size = Pt(14)
    h2.font.bold = True
    h2.font.color.rgb = RGBColor(0, 0, 0)
    h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.keep_with_next = True
    h2.paragraph_format.first_line_indent = Cm(0)

    # 4. Heading 3
    h3 = styles['Heading 3']
    h3.font.name = 'Times New Roman'
    h3.font.size = Pt(13)
    h3.font.bold = True
    h3.font.color.rgb = RGBColor(0, 0, 0)
    h3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    h3.paragraph_format.space_before = Pt(6)
    h3.paragraph_format.space_after = Pt(6)
    h3.paragraph_format.keep_with_next = True
    h3.paragraph_format.first_line_indent = Cm(0)


def setup_page_layout(section):
    """Cấu hình khổ giấy A4 và lề trang chuẩn."""
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3.5)
    section.right_margin = Cm(2.0)
    section.header_distance = Cm(1.5)
    section.footer_distance = Cm(1.5)

    # Thêm số trang ở chân trang (Footer Bottom Center)
    footer = section.footer
    footer_p = footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_p.paragraph_format.first_line_indent = Cm(0)
    add_field(footer_p, "PAGE")


def create_blank_academic_template(output_path: str) -> str:
    """Tạo một file template Word (.docx) sạch với toàn bộ styles đã định hình."""
    doc = Document()
    setup_page_layout(doc.sections[0])
    setup_document_styles(doc)

    p = doc.add_paragraph("MẪU BÁO CÁO HỌC THUẬT CHUẨN ĐẠI HỌC", style='Heading 1')
    p.paragraph_format.page_break_before = False
    
    doc.add_paragraph("Tài liệu này đã được cấu hình toàn bộ thông số định dạng chuẩn:")
    doc.add_paragraph("- Khổ giấy: A4 (21 x 29.7 cm)")
    doc.add_paragraph("- Căn lề: Top 2.5cm, Bottom 2.5cm, Left 3.5cm, Right 2.0cm")
    doc.add_paragraph("- Thân bài: Times New Roman 13pt, Justified, 1.5 lines, First-line indent 1.27cm, Spacing after 6pt")
    doc.add_paragraph("- Tiêu đề: Heading 1 (16pt In hoa Căn giữa), Heading 2 (14pt Đậm), Heading 3 (13pt Đậm)")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    return output_path


if __name__ == "__main__":
    out = "C:/Users/TAN/.gemini/config/skills/academic-report-generator/templates/Academic_Report_Template.docx"
    create_blank_academic_template(out)
    print(f"Đã tạo file template thành công tại: {out}")
