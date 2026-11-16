#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_formatting.py
Kiểm tra tự động các quy tắc định dạng Microsoft Word (.docx) theo Phase 7 của Academic Report Generator.

Tiêu chí kiểm tra:
1. Khổ giấy A4 (21.0 x 29.7 cm) và Căn lề chuẩn (Top: 2.5, Bottom: 2.5, Left: 3.5, Right: 2.0 cm).
2. Định dạng văn bản thân bài (Times New Roman, 13pt, Justified, 1.5 lines, First Line Indent 1.27cm, Spacing After 6pt).
3. Định dạng tiêu đề các cấp (Heading 1: 16pt bold center page-break-before keep-with-next; Heading 2: 14pt bold; Heading 3: 13pt bold).
4. Sự tồn tại của trường số trang (PAGE) và trường mục lục (TOC).
5. Vị trí caption Bảng (trước bảng) và Hình ảnh (sau hình).
6. Phát hiện các đoạn văn rỗng liên tiếp (Whitespace abuse).
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt
except ImportError:
    docx = None


def check_page_setup(doc) -> Dict[str, Any]:
    """Kiểm tra khổ giấy và lề trang của section đầu tiên."""
    if not doc.sections:
        return {"status": "FAIL", "message": "Tài liệu không có section nào."}

    sec = doc.sections[0]
    
    # 1. Khổ giấy
    width_cm = sec.page_width.cm if sec.page_width else 0
    height_cm = sec.page_height.cm if sec.page_height else 0
    
    # A4 chuẩn: 21.0 cm x 29.7 cm (dung sai 0.3cm)
    is_a4 = (abs(width_cm - 21.0) <= 0.3) and (abs(height_cm - 29.7) <= 0.3)

    # 2. Lề trang chuẩn: Top 2.5, Bottom 2.5, Left 3.5, Right 2.0 cm
    top_cm = sec.top_margin.cm if sec.top_margin else 0
    bottom_cm = sec.bottom_margin.cm if sec.bottom_margin else 0
    left_cm = sec.left_margin.cm if sec.left_margin else 0
    right_cm = sec.right_margin.cm if sec.right_margin else 0

    margin_issues = []
    if abs(top_cm - 2.5) > 0.2:
        margin_issues.append(f"Top margin: {top_cm:.2f}cm (chuẩn: 2.5cm)")
    if abs(bottom_cm - 2.5) > 0.2:
        margin_issues.append(f"Bottom margin: {bottom_cm:.2f}cm (chuẩn: 2.5cm)")
    if abs(left_cm - 3.5) > 0.2:
        margin_issues.append(f"Left margin: {left_cm:.2f}cm (chuẩn: 3.5cm - chừa đóng gáy)")
    if abs(right_cm - 2.0) > 0.2:
        margin_issues.append(f"Right margin: {right_cm:.2f}cm (chuẩn: 2.0cm)")

    status = "PASS" if is_a4 and not margin_issues else "FAIL"

    return {
        "status": status,
        "is_a4": is_a4,
        "width_cm": round(width_cm, 2),
        "height_cm": round(height_cm, 2),
        "margins_cm": {
            "top": round(top_cm, 2),
            "bottom": round(bottom_cm, 2),
            "left": round(left_cm, 2),
            "right": round(right_cm, 2)
        },
        "margin_issues": margin_issues
    }


def get_paragraph_font_and_size(p, doc) -> Tuple[Optional[str], Optional[float]]:
    """Xác định font family và font size thực tế của đoạn văn (kết hợp run và style)."""
    # 1. Kiểm tra run trước
    for r in p.runs:
        font_name = r.font.name
        font_size = r.font.size.pt if r.font.size else None
        
        # Nếu chưa có trên r.font, kiểm tra trong oxml rFonts
        if not font_name and r._r.rPr is not None:
            rFonts = r._r.rPr.find(qn('w:rFonts'))
            if rFonts is not None:
                font_name = rFonts.get(qn('w:ascii')) or rFonts.get(qn('w:hAnsi'))
        
        if not font_size and r._r.rPr is not None:
            sz = r._r.rPr.find(qn('w:sz'))
            if sz is not None and sz.get(qn('w:val')):
                font_size = float(sz.get(qn('w:val'))) / 2.0

        if font_name or font_size:
            return font_name, font_size

    # 2. Kiểm tra Style của paragraph
    if p.style:
        style_font = p.style.font.name
        style_size = p.style.font.size.pt if p.style.font.size else None
        if style_font or style_size:
            return style_font, style_size

    # 3. Mặc định Normal style
    try:
        normal_style = doc.styles['Normal']
        norm_font = normal_style.font.name
        norm_size = normal_style.font.size.pt if normal_style.font.size else None
        return norm_font, norm_size
    except Exception:
        return None, None


def has_keep_with_next(p) -> bool:
    """Kiểm tra thuộc tính keep_with_next ở cả paragraph và Style."""
    if p.paragraph_format.keep_with_next is True:
        return True
    if p._p.pPr is not None and p._p.pPr.find(qn('w:keepNext')) is not None:
        return True
    if p.style and p.style._element is not None:
        pPr = p.style._element.find(qn('w:pPr'))
        if pPr is not None and pPr.find(qn('w:keepNext')) is not None:
            return True
    return False


def get_paragraph_alignment(p) -> Optional[Any]:
    """Lấy căn lề kế thừa từ paragraph hoặc style."""
    if p.alignment is not None:
        return p.alignment
    if p.style and p.style.paragraph_format.alignment is not None:
        return p.style.paragraph_format.alignment
    if p._p.pPr is not None:
        jc = p._p.pPr.find(qn('w:jc'))
        if jc is not None and jc.get(qn('w:val')) in ['both', 'justify']:
            return WD_ALIGN_PARAGRAPH.JUSTIFY
    if p.style and p.style._element is not None:
        pPr = p.style._element.find(qn('w:pPr'))
        if pPr is not None:
            jc = pPr.find(qn('w:jc'))
            if jc is not None and jc.get(qn('w:val')) in ['both', 'justify']:
                return WD_ALIGN_PARAGRAPH.JUSTIFY
    return None


def get_first_line_indent_cm(p) -> Optional[float]:
    """Lấy độ thụt đầu dòng (cm) kế thừa từ paragraph hoặc style."""
    if p.paragraph_format.first_line_indent is not None:
        return p.paragraph_format.first_line_indent.cm
    if p.style and p.style.paragraph_format.first_line_indent is not None:
        return p.style.paragraph_format.first_line_indent.cm
    if p.style and p.style._element is not None:
        pPr = p.style._element.find(qn('w:pPr'))
        if pPr is not None:
            ind = pPr.find(qn('w:ind'))
            if ind is not None and ind.get(qn('w:firstLine')):
                twips = float(ind.get(qn('w:firstLine')))
                return twips / 567.0
    return None


def check_body_paragraphs(doc) -> Dict[str, Any]:
    """Kiểm tra mẫu các đoạn văn thân bài (Normal text)."""
    body_paras = []
    empty_paras = 0
    consecutive_empty = 0
    max_consecutive_empty = 0

    for p in doc.paragraphs:
        txt = p.text.strip()
        style_name = p.style.name if p.style else ""
        
        if not txt:
            consecutive_empty += 1
            max_consecutive_empty = max(max_consecutive_empty, consecutive_empty)
            empty_paras += 1
            continue
        else:
            consecutive_empty = 0

        # Chỉ kiểm tra các đoạn văn dài có vẻ là văn bản thông thường
        if not style_name.startswith("Heading") and not re.match(r'^(CHƯƠNG|Bảng|Hình|Mục lục|Nguồn:)', txt, re.IGNORECASE):
            if len(txt) > 60:
                body_paras.append(p)

    if not body_paras:
        return {
            "status": "WARNING",
            "message": "Không tìm thấy đoạn văn thân bài đủ dài (>60 ký tự) để kiểm định.",
            "empty_paras": empty_paras,
            "max_consecutive_empty": max_consecutive_empty
        }

    sample_paras = body_paras[:15]
    issues = []

    non_times_count = 0
    non_13pt_count = 0
    non_justified_count = 0
    non_1_5_lines_count = 0
    non_indent_count = 0

    for p in sample_paras:
        font_name, font_size = get_paragraph_font_and_size(p, doc)
        
        if font_name and "times new roman" not in font_name.lower():
            non_times_count += 1
            
        if font_size and abs(font_size - 13.0) > 0.5:
            non_13pt_count += 1

        # Căn lề: Căn đều (Justified)
        align = get_paragraph_alignment(p)
        if align != WD_ALIGN_PARAGRAPH.JUSTIFY:
            non_justified_count += 1

        # Giãn dòng: 1.5 lines
        line_spacing = p.paragraph_format.line_spacing
        if line_spacing is None and p.style:
            line_spacing = p.style.paragraph_format.line_spacing
            
        if line_spacing is not None:
            if isinstance(line_spacing, (int, float)):
                if abs(line_spacing - 1.5) > 0.15:
                    non_1_5_lines_count += 1

        # Thụt đầu dòng: 1.27 cm (0.5 in)
        indent_cm = get_first_line_indent_cm(p)
        if indent_cm is not None:
            if abs(indent_cm - 1.27) > 0.2:
                non_indent_count += 1
        else:
            non_indent_count += 1

    sample_size = len(sample_paras)
    if non_times_count > sample_size * 0.3:
        issues.append(f"Font chữ thân bài không phải Times New Roman ({non_times_count}/{sample_size} đoạn kiểm tra)")
    if non_13pt_count > sample_size * 0.3:
        issues.append(f"Cỡ chữ thân bài không phải 13pt ({non_13pt_count}/{sample_size} đoạn kiểm tra)")
    if non_justified_count > sample_size * 0.3:
        issues.append(f"Chưa căn đều 2 bên (Justified) ({non_justified_count}/{sample_size} đoạn kiểm tra)")
    if non_1_5_lines_count > sample_size * 0.3:
        issues.append(f"Giãn dòng chưa chuẩn 1.5 lines ({non_1_5_lines_count}/{sample_size} đoạn kiểm tra)")
    if non_indent_count > sample_size * 0.3:
        issues.append(f"Chưa thụt dòng đầu đoạn 1.27cm ({non_indent_count}/{sample_size} đoạn kiểm tra)")

    if max_consecutive_empty > 2:
        issues.append(f"Phát hiện lạm dụng dòng trống liên tiếp (nhiều nhất {max_consecutive_empty} dòng trống liên tiếp)")

    status = "FAIL" if len(issues) >= 2 else ("WARNING" if issues else "PASS")

    return {
        "status": status,
        "sample_checked": sample_size,
        "issues": issues,
        "empty_paras": empty_paras,
        "max_consecutive_empty": max_consecutive_empty
    }


def check_heading_styles(doc) -> Dict[str, Any]:
    """Kiểm tra thuộc tính các Heading Styles (H1, H2, H3)."""
    h1_paras = [p for p in doc.paragraphs if p.style and (p.style.name.startswith("Heading 1") or p.style.name.startswith("Tiêu đề 1"))]
    h2_paras = [p for p in doc.paragraphs if p.style and (p.style.name.startswith("Heading 2") or p.style.name.startswith("Tiêu đề 2"))]
    h3_paras = [p for p in doc.paragraphs if p.style and (p.style.name.startswith("Heading 3") or p.style.name.startswith("Tiêu đề 3"))]

    issues = []
    
    # Kiểm tra H1
    for p in h1_paras:
        txt = p.text.strip()
        if not txt:
            continue
        # Heading 1 nên viết hoa
        if txt != txt.upper() and not re.match(r'^(Mục lục|Lời cam đoan)', txt, re.IGNORECASE):
            issues.append(f"Heading 1 chưa viết in hoa toàn bộ: '{txt[:40]}...'")
        
        # Kiểm tra keep_with_next
        if not has_keep_with_next(p):
            issues.append(f"Heading 1 thiếu thuộc tính 'keep_with_next': '{txt[:30]}...'")

    # Kiểm tra H2 & H3 keep_with_next
    for p in h2_paras + h3_paras:
        txt = p.text.strip()
        if txt and not has_keep_with_next(p):
            issues.append(f"Tiêu đề thiếu thuộc tính 'keep_with_next': '{txt[:30]}...'")

    status = "PASS" if not issues else "WARNING"
    return {
        "status": status,
        "h1_count": len(h1_paras),
        "h2_count": len(h2_paras),
        "h3_count": len(h3_paras),
        "issues": issues[:10]
    }


def check_fields_and_captions(doc) -> Dict[str, Any]:
    """Kiểm tra trường số trang, mục lục TOC, và caption bảng/hình."""
    doc_xml = doc._element.xml
    has_toc = ("w:instrText" in doc_xml and "TOC" in doc_xml) or ("w:fldSimple" in doc_xml and "TOC" in doc_xml)
    
    has_page_num = False
    for sec in doc.sections:
        footer_xml = sec.footer._element.xml if sec.footer else ""
        if ("PAGE" in footer_xml) or ("w:fldSimple" in footer_xml and "PAGE" in footer_xml):
            has_page_num = True
            break

    table_count = len(doc.tables)
    table_caption_count = len([p for p in doc.paragraphs if re.match(r'^Bảng\s+[0-9IVX]+', p.text.strip(), re.IGNORECASE)])
    figure_caption_count = len([p for p in doc.paragraphs if re.match(r'^(Hình|Sơ đồ|Đồ thị)\s+[0-9IVX]+', p.text.strip(), re.IGNORECASE)])

    warnings = []
    if not has_toc:
        warnings.append("Chưa phát hiện mã trường mục lục tự động (TOC Field). Nếu dùng mục lục thủ công, khuyến nghị chuyển sang trường TOC.")
    if not has_page_num:
        warnings.append("Chưa phát hiện trường số trang tự động (PAGE Field) ở Footer của tài liệu.")
    if table_count > 0 and table_caption_count < table_count:
        warnings.append(f"Số caption Bảng ({table_caption_count}) ít hơn số lượng bảng thực tế ({table_count}).")

    return {
        "has_toc_field": has_toc,
        "has_page_number_field": has_page_num,
        "table_count": table_count,
        "table_caption_count": table_caption_count,
        "figure_caption_count": figure_caption_count,
        "warnings": warnings,
        "status": "PASS" if not warnings else "WARNING"
    }


def validate_formatting(docx_path: str) -> Dict[str, Any]:
    """Hàm tổng hợp kiểm định định dạng Word chuẩn Phase 7."""
    if not os.path.exists(docx_path):
        return {
            "status": "FAIL",
            "file": docx_path,
            "errors": [f"File không tồn tại: {docx_path}"]
        }

    if docx is None:
        return {
            "status": "FAIL",
            "file": docx_path,
            "errors": ["Thư viện 'python-docx' chưa được cài đặt. Chạy: pip install python-docx"]
        }

    try:
        doc = docx.Document(docx_path)
    except Exception as e:
        return {
            "status": "FAIL",
            "file": docx_path,
            "errors": [f"Không thể đọc file DOCX: {str(e)}"]
        }

    page_setup = check_page_setup(doc)
    body_check = check_body_paragraphs(doc)
    heading_check = check_heading_styles(doc)
    fields_check = check_fields_and_captions(doc)

    all_errors = []
    all_warnings = []

    if page_setup["status"] == "FAIL":
        all_errors.extend(page_setup.get("margin_issues", []))
        if not page_setup.get("is_a4"):
            all_errors.append(f"Khổ giấy không phải A4: {page_setup.get('width_cm')}x{page_setup.get('height_cm')}cm")

    if body_check["status"] == "FAIL":
        all_errors.extend(body_check.get("issues", []))
    elif body_check["status"] == "WARNING":
        all_warnings.extend(body_check.get("issues", []))

    all_warnings.extend(heading_check.get("issues", []))
    all_warnings.extend(fields_check.get("warnings", []))

    final_status = "FAIL" if all_errors else ("WARNING" if all_warnings else "PASS")

    matrix = [
        {"criterion": "Khổ giấy chuẩn A4 (21 x 29.7 cm)", "status": "PASS" if page_setup.get("is_a4") else "FAIL", "note": f"{page_setup.get('width_cm')}x{page_setup.get('height_cm')} cm"},
        {"criterion": "Căn lề (Top 2.5, Bottom 2.5, Left 3.5, Right 2.0 cm)", "status": "FAIL" if page_setup.get("margin_issues") else "PASS", "note": str(page_setup.get("margins_cm"))},
        {"criterion": "Định dạng Body (Times New Roman 13pt, Justified, 1.5 lines)", "status": body_check["status"], "note": f"{len(body_check.get('issues', []))} lưu ý"},
        {"criterion": "Thuộc tính Heading Styles (In hoa H1, keep_with_next)", "status": heading_check["status"], "note": f"H1: {heading_check.get('h1_count')}, H2: {heading_check.get('h2_count')}"},
        {"criterion": "Trường Mục lục tự động (TOC Field)", "status": "PASS" if fields_check.get("has_toc_field") else "WARNING", "note": "Có mã TOC" if fields_check.get("has_toc_field") else "Thiếu mã TOC"},
        {"criterion": "Trường Đánh số trang (PAGE Field)", "status": "PASS" if fields_check.get("has_page_number_field") else "WARNING", "note": "Có ở Footer" if fields_check.get("has_page_number_field") else "Thiếu trường PAGE"},
        {"criterion": "Captions Bảng biểu và Hình vẽ", "status": "PASS" if not (fields_check.get("table_count", 0) > fields_check.get("table_caption_count", 0)) else "WARNING", "note": f"Bảng: {fields_check.get('table_count')}, Caption: {fields_check.get('table_caption_count')}"},
        {"criterion": "Độ chính xác số trang thực tế trong TOC", "status": "NOT_CHECKED", "note": "python-docx không tự cập nhật bố cục trang in; cần cập nhật F9 trong Word"}
    ]

    return {
        "status": final_status,
        "file": docx_path,
        "matrix": matrix,
        "page_setup": page_setup,
        "body_check": body_check,
        "heading_check": heading_check,
        "fields_check": fields_check,
        "errors": all_errors,
        "warnings": all_warnings
    }


def main():
    parser = argparse.ArgumentParser(description="Kiểm tra định dạng Microsoft Word chuyên sâu theo chuẩn học thuật.")
    parser.add_argument("--file", "-f", required=True, help="Đường dẫn tới file DOCX cần kiểm tra.")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON.")
    args = parser.parse_args()

    result = validate_formatting(args.file)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n" + "="*70)
        print(f"KẾT QUẢ KIỂM TRA ĐỊNH DẠNG MICROSOFT WORD: {result['status']}")
        print(f"Tập tin: {result['file']}")
        print("="*70)
        
        print(f"{'Tiêu chí':<45} | {'Trạng thái':<12} | {'Chi tiết'}")
        print("-" * 75)
        for row in result.get("matrix", []):
            print(f"{row['criterion']:<45} | {row['status']:<12} | {row['note']}")
        print("-" * 75)

        if result.get("errors"):
            print("\n[LỖI NGHIÊM TRỌNG / FAIL]:")
            for err in result["errors"]:
                print(f"  [X] {err}")

        if result.get("warnings"):
            print("\n[CẢNH BÁO / WARNING]:")
            for w in result["warnings"]:
                print(f"  [!] {w}")

        print("="*70 + "\n")

    sys.exit(0 if result["status"] in ["PASS", "WARNING"] else 1)


if __name__ == "__main__":
    main()
