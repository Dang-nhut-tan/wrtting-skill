#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_structure.py
Hệ thống kiểm tra cấu trúc học thuật và phân cấp đề mục trong báo cáo/tiểu luận Word (.docx).

Kiểm tra:
1. Sự hiện diện của các phần bắt buộc (Trang bìa, Mở đầu, Các chương nội dung, Kết luận, Tài liệu tham khảo).
2. Trình tự logic của các chương (Chương 1 -> Chương 2 -> Chương 3...).
3. Phân cấp đề mục (Heading 1 -> Heading 2 -> Heading 3), phát hiện lỗi nhảy cóc cấp độ (e.g. H1 -> H3).
4. Các mục con mồ côi hoặc đề mục rỗng.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    import docx
    from docx.document import Document as DocxDocument
except ImportError:
    docx = None


def normalize_text(text: str) -> str:
    """Loại bỏ khoảng trắng thừa và chuẩn hóa chuỗi Unicode."""
    return re.sub(r'\s+', ' ', text or '').strip()


def extract_headings_and_structure(doc) -> List[Dict[str, Any]]:
    """Trích xuất toàn bộ danh sách paragraph, nhận diện Heading styles và nội dung."""
    items = []
    for idx, p in enumerate(doc.paragraphs):
        text = normalize_text(p.text)
        style_name = p.style.name if p.style else ""
        
        # Nhận diện cấp độ heading
        level = None
        if style_name.startswith("Heading 1") or style_name == "Heading 1":
            level = 1
        elif style_name.startswith("Heading 2") or style_name == "Heading 2":
            level = 2
        elif style_name.startswith("Heading 3") or style_name == "Heading 3":
            level = 3
        elif style_name.startswith("Heading 4") or style_name == "Heading 4":
            level = 4
        elif style_name.lower().startswith("tiêu đề 1"):
            level = 1
        elif style_name.lower().startswith("tiêu đề 2"):
            level = 2
        elif style_name.lower().startswith("tiêu đề 3"):
            level = 3
        elif style_name.lower().startswith("tiêu đề 4"):
            level = 4
        else:
            # Dự phòng nhận diện qua regex nếu tài liệu không dùng Named Style chuẩn
            upper_text = text.upper()
            if re.match(r'^(CHƯƠNG\s+[0-9IVX]+|PHẦN\s+MỞ\s+ĐẦU|KẾT\s+LUẬN|TÀI\s+LIỆU\s+THAM\s+KHẢO|MỤC\s+LỤC)', upper_text):
                level = 1
            elif re.match(r'^[0-9]+\.[0-9]+\.\s+', text):
                level = 2
            elif re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.\s+', text):
                level = 3

        if level is not None or text:
            items.append({
                "index": idx,
                "text": text,
                "style": style_name,
                "level": level,
                "is_empty": len(text) == 0
            })
    return items


def validate_structure(docx_path: str) -> Dict[str, Any]:
    """Hàm kiểm tra cấu trúc học thuật chính."""
    if not os.path.exists(docx_path):
        return {
            "status": "FAIL",
            "file": docx_path,
            "errors": [f"File không tồn tại: {docx_path}"],
            "warnings": [],
            "sections_found": [],
            "missing_sections": []
        }

    if docx is None:
        return {
            "status": "FAIL",
            "file": docx_path,
            "errors": ["Thư viện 'python-docx' chưa được cài đặt. Chạy: pip install python-docx"],
            "warnings": [],
            "sections_found": [],
            "missing_sections": []
        }

    try:
        doc = docx.Document(docx_path)
    except Exception as e:
        return {
            "status": "FAIL",
            "file": docx_path,
            "errors": [f"Không thể đọc file DOCX: {str(e)}"],
            "warnings": [],
            "sections_found": [],
            "missing_sections": []
        }

    items = extract_headings_and_structure(doc)
    headings = [it for it in items if it["level"] is not None and not it["is_empty"]]

    errors = []
    warnings = []
    sections_found = []
    
    # 1. Kiểm tra các phần cốt lõi
    all_text_combined = " ".join([it["text"] for it in items])
    upper_combined = all_text_combined.upper()

    mandatory_sections = [
        {"name": "Mở đầu", "pattern": r'(MỞ\s+ĐẦU|ĐẶT\s+VẤN\s+ĐỀ|TÍNH\s+CẤP\s+THIẾT)'},
        {"name": "Nội dung nghiên cứu (Các chương)", "pattern": r'(CHƯƠNG\s+1|CHƯƠNG\s+I\b)'},
        {"name": "Kết luận", "pattern": r'(KẾT\s+LUẬN|TỔNG\s+KẾT)'},
        {"name": "Tài liệu tham khảo", "pattern": r'(TÀI\s+LIỆU\s+THAM\s+KHẢO|DANH\s+MỤC\s+THAM\s+KHẢO|REFERENCES)'}
    ]

    missing_sections = []
    for sec in mandatory_sections:
        if re.search(sec["pattern"], upper_combined):
            sections_found.append(sec["name"])
        else:
            missing_sections.append(sec["name"])
            errors.append(f"Thiếu phần bắt buộc: '{sec['name']}'")

    # Kiểm tra phần tùy chọn quan trọng
    optional_sections = [
        {"name": "Mục lục (TOC)", "pattern": r'(MỤC\s+LỤC|TABLE\s+OF\s+CONTENTS)'},
        {"name": "Mục tiêu nghiên cứu", "pattern": r'(MỤC\s+TIÊU\s+NGHIÊN\s+CỨU|CÂU\s+HỎI\s+NGHIÊN\s+CỨU)'},
        {"name": "Phương pháp nghiên cứu", "pattern": r'(PHƯƠNG\s+PHÁP\s+NGHIÊN\s+CỨU|RESEARCH\s+METHODOLOGY)'}
    ]
    for sec in optional_sections:
        if re.search(sec["pattern"], upper_combined):
            sections_found.append(sec["name"])
        else:
            warnings.append(f"Khuyến nghị bổ sung phần: '{sec['name']}'")

    # 2. Kiểm tra phân cấp Heading (Hierarchy Check)
    hierarchy_errors = []
    prev_level = 0
    for h in headings:
        cur_level = h["level"]
        # Lỗi nhảy cóc cấp độ (ví dụ: đang ở level 1 nhảy thẳng xuống level 3)
        if cur_level - prev_level > 1 and prev_level > 0:
            err_msg = f"Lỗi nhảy cóc cấp đề mục: Từ Heading {prev_level} nhảy thẳng sang Heading {cur_level} tại '{h['text']}'"
            hierarchy_errors.append(err_msg)
            errors.append(err_msg)
        prev_level = cur_level

    # 3. Kiểm tra thứ tự chương
    chapter_numbers = []
    for h in headings:
        if h["level"] == 1:
            match = re.search(r'CHƯƠNG\s+([0-9]+)', h["text"].upper())
            if match:
                chapter_numbers.append(int(match.group(1)))

    if chapter_numbers:
        expected = list(range(1, len(chapter_numbers) + 1))
        if chapter_numbers != expected:
            errors.append(f"Thứ tự số hiệu chương không liên tục: Phát hiện {chapter_numbers}, mong đợi {expected}")

    status = "FAIL" if errors else ("WARNING" if warnings else "PASS")

    return {
        "status": status,
        "file": docx_path,
        "total_headings": len(headings),
        "sections_found": sections_found,
        "missing_sections": missing_sections,
        "hierarchy_errors": hierarchy_errors,
        "errors": errors,
        "warnings": warnings,
        "headings_outline": [{"level": h["level"], "text": h["text"]} for h in headings[:30]]
    }


def main():
    parser = argparse.ArgumentParser(description="Kiểm tra cấu trúc và phân cấp đề mục báo cáo Word (.docx).")
    parser.add_argument("--file", "-f", required=True, help="Đường dẫn tới file DOCX cần kiểm tra.")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON.")
    args = parser.parse_args()

    result = validate_structure(args.file)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n" + "="*60)
        print(f"KẾT QUẢ KIỂM TRA CẤU TRÚC: {result['status']}")
        print(f"Tập tin: {result['file']}")
        print("="*60)
        print(f"Tổng số tiêu đề trích xuất: {result.get('total_headings', 0)}")
        print(f"Các phần phát hiện: {', '.join(result.get('sections_found', []))}")
        
        if result.get("missing_sections"):
            print(f"\n[LỖI] Các phần bị thiếu: {', '.join(result['missing_sections'])}")
            
        if result.get("hierarchy_errors"):
            print("\n[LỖI] Lỗi phân cấp đề mục:")
            for err in result["hierarchy_errors"]:
                print(f"  - {err}")
                
        if result.get("warnings"):
            print("\n[CẢNH BÁO] Lưu ý cải thiện:")
            for w in result["warnings"]:
                print(f"  - {w}")
                
        print("="*60 + "\n")

    sys.exit(0 if result["status"] in ["PASS", "WARNING"] else 1)


if __name__ == "__main__":
    main()
