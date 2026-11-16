#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_citations.py
Kiểm tra tính toàn vẹn và nhất quán của hệ thống trích dẫn (APA 7th, IEEE) trong báo cáo Word (.docx).

Kiểm tra:
1. Trích dẫn mồ côi ngược (In-text citations không có trong danh mục tham khảo).
2. Tài liệu mồ côi xuôi (Tài liệu trong danh mục tham khảo không được viện dẫn trong bài).
3. Phát hiện cờ cảnh báo [NEEDS_VERIFICATION] hoặc dấu hiệu ngụy tạo nguồn.
4. Tuyên bố rõ ràng: Chỉ kiểm tra tính khớp nối văn bản, không giả định đã xác minh nguồn ngoài đời thực nếu chưa tra cứu CSDL học thuật.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Set, Tuple

try:
    import docx
except ImportError:
    docx = None


# Regex nhận diện trích dẫn APA 7 trong ngoặc: (Tác giả, Năm) hoặc (Tác giả 1 & Tác giả 2, Năm)
# Không cho phép vượt qua dòng mới
APA_PARENTHETICAL_PATTERN = re.compile(
    r'\(([A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵA-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ\s&,\.\-–—]+?(?:et\s+al\.|và\s+cộng\s+sự|và\s+ctg\.)?),?\s+([12][0-9]{3}|n\.d\.|k\.n\.)(?:\s*,\s*tr\.\s*[0-9\-]+|\s*,\s*p\.\s*[0-9\-]+)?\)'
)

# Regex nhận diện trích dẫn APA 7 dạng tường thuật: Tác giả (Năm)
APA_NARRATIVE_PATTERN = re.compile(
    r'([A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵA-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ\s&]+?(?:et\s+al\.|và\s+cộng\s+sự|và\s+ctg\.)?)\s+\(([12][0-9]{3}|n\.d\.|k\.n\.)\)'
)

# Regex nhận diện trích dẫn IEEE: [1], [2], [1-3], [1, 2]
IEEE_CITATION_PATTERN = re.compile(r'\[([0-9]+(?:\s*[\-,]\s*[0-9]+)*)\]')


def split_body_and_references(paragraphs: List[Any]) -> Tuple[List[str], List[str]]:
    """Phân tách nội dung thân bài và danh mục tài liệu tham khảo."""
    body_paras = []
    ref_paras = []
    is_ref_section = False

    ref_header_pattern = re.compile(r'^(TÀI\s+LIỆU\s+THAM\s+KHẢO|DANH\s+MỤC\s+THAM\s+KHẢO|REFERENCES|BIBLIOGRAPHY)', re.IGNORECASE)

    for p in paragraphs:
        text = p.text.strip()
        if not text:
            continue
        
        # Kiểm tra tiêu đề chuyển sang mục tham khảo
        if ref_header_pattern.match(text):
            is_ref_section = True
            continue

        if is_ref_section:
            # Nếu gặp phụ lục thì kết thúc mục tham khảo
            if re.match(r'^(PHỤ\s+LỤC|APPENDIX)', text, re.IGNORECASE):
                is_ref_section = False
                body_paras.append(text)
            else:
                ref_paras.append(text)
        else:
            body_paras.append(text)

    return body_paras, ref_paras


def extract_in_text_citations_from_paras(body_paras: List[str]) -> Dict[str, Any]:
    """Trích xuất toàn bộ các trích dẫn in-text xuất hiện trong từng đoạn thân bài."""
    apa_citations = []
    ieee_numbers = []

    for p_text in body_paras:
        # 1. Trích dẫn APA trong ngoặc
        for match in APA_PARENTHETICAL_PATTERN.finditer(p_text):
            raw_author, year = match.groups()
            # Loại trừ nguồn số liệu nội bộ (tác giả tự làm)
            if re.search(r'\b(tác\s+giả|nhóm\s+tác\s+giả|nhóm\s+nghiên\s+cứu)\b', raw_author, re.IGNORECASE):
                continue
            # Xử lý trường hợp nhiều tác giả cách nhau bởi dấu chấm phẩy
            sub_sources = raw_author.split(';')
            for src in sub_sources:
                src = src.strip()
                if src:
                    apa_citations.append({
                        "raw": match.group(0),
                        "author": src,
                        "year": year,
                        "type": "parenthetical"
                    })

        # 2. Trích dẫn APA tường thuật
        for match in APA_NARRATIVE_PATTERN.finditer(p_text):
            raw_author, year = match.groups()
            raw_author = raw_author.strip()
            
            # Bỏ qua nguồn số liệu sơ cấp do tác giả tự khảo sát
            if re.search(r'\b(tác\s+giả|nhóm\s+tác\s+giả|nhóm\s+nghiên\s+cứu|khảo\s+sát\s+của)\b', raw_author, re.IGNORECASE):
                continue

            # Bóc tách các từ dẫn đề mở đầu câu: "Theo nghiên cứu của Lê Văn C" -> "Lê Văn C"
            author_clean = re.sub(
                r'^(Theo\s+(?:kết\s+quả\s+)?(?:nghiên\s+cứu\s+(?:của\s+)?)?|Ngoài\s+ra\s+(?:mô\s+hình\s+(?:của\s+)?)?|Mô\s+hình\s+(?:của\s+)?|Nghiên\s+cứu\s+(?:của\s+)?|Khảo\s+sát\s+(?:của\s+)?|Theo\s+)',
                '',
                raw_author,
                flags=re.IGNORECASE
            ).strip()

            # Loại trừ các cụm từ phổ biến không phải tên người
            if author_clean and not re.search(r'\b(Bảng|Hình|Sơ đồ|Chương|Mục|Trong)\b', author_clean):
                apa_citations.append({
                    "raw": f"{author_clean} ({year})",
                    "author": author_clean,
                    "year": year,
                    "type": "narrative"
                })

        # 3. Trích dẫn IEEE
        for match in IEEE_CITATION_PATTERN.finditer(p_text):
            raw_nums = match.group(1)
            parts = re.split(r'[,]', raw_nums)
            for part in parts:
                part = part.strip()
                if '-' in part:
                    sub = part.split('-')
                    if len(sub) == 2 and sub[0].strip().isdigit() and sub[1].strip().isdigit():
                        start, end = int(sub[0]), int(sub[1])
                        ieee_numbers.extend(list(range(start, end + 1)))
                elif part.isdigit():
                    ieee_numbers.append(int(part))

    return {
        "apa_citations": apa_citations,
        "ieee_numbers": sorted(list(set(ieee_numbers)))
    }


def parse_reference_entries(ref_paras: List[str]) -> List[Dict[str, Any]]:
    """Phân tích các mục trong danh mục tài liệu tham khảo."""
    entries = []
    for idx, text in enumerate(ref_paras):
        # Trích xuất năm xuất bản
        year_match = re.search(r'\(([12][0-9]{3}|n\.d\.|k\.n\.)\)', text)
        year = year_match.group(1) if year_match else None
        
        # Trích xuất số thứ tự IEEE nếu có [1]
        ieee_match = re.match(r'^\[([0-9]+)\]', text)
        ieee_num = int(ieee_match.group(1)) if ieee_match else None

        # Trích xuất tên tác giả (phần trước năm)
        author_part = text
        if year_match:
            author_part = text[:year_match.start()].strip()
            author_part = re.sub(r'^[0-9]+\.\s*', '', author_part) # bỏ số thứ tự nếu có
            author_part = re.sub(r'^\[[0-9]+\]\s*', '', author_part)

        entries.append({
            "index": idx + 1,
            "raw_text": text,
            "author_part": author_part.strip(),
            "year": year,
            "ieee_num": ieee_num,
            "has_needs_verification": "NEEDS_VERIFICATION" in text
        })
    return entries


def clean_author_for_matching(author_str: str) -> str:
    """Rút gọn tên tác giả để so khớp mềm."""
    s = author_str.lower()
    s = re.sub(r'(et\s+al\.|và\s+cộng\s+sự|và\s+ctg\.)', '', s)
    s = re.sub(r'[\(\)\[\],&]', ' ', s)
    tokens = [t.strip() for t in s.split() if len(t.strip()) > 1]
    return " ".join(tokens)


def validate_citations(docx_path: str) -> Dict[str, Any]:
    """Hàm kiểm tra trích dẫn chính."""
    if not os.path.exists(docx_path):
        return {
            "status": "FAIL",
            "file": docx_path,
            "errors": [f"File không tồn tại: {docx_path}"],
            "warnings": []
        }

    if docx is None:
        return {
            "status": "FAIL",
            "file": docx_path,
            "errors": ["Thư viện 'python-docx' chưa được cài đặt. Chạy: pip install python-docx"],
            "warnings": []
        }

    try:
        doc = docx.Document(docx_path)
    except Exception as e:
        return {
            "status": "FAIL",
            "file": docx_path,
            "errors": [f"Không thể đọc file DOCX: {str(e)}"],
            "warnings": []
        }

    body_paras, ref_paras = split_body_and_references(doc.paragraphs)
    
    extracted_in_text = extract_in_text_citations_from_paras(body_paras)
    apa_in_text = extracted_in_text["apa_citations"]
    ieee_in_text = extracted_in_text["ieee_numbers"]

    ref_entries = parse_reference_entries(ref_paras)

    errors = []
    warnings = []

    # Kiểm tra cờ nghi vấn NEEDS_VERIFICATION
    unverified_flags = []
    for idx, p in enumerate(doc.paragraphs):
        if "NEEDS_VERIFICATION" in p.text:
            unverified_flags.append({
                "paragraph_index": idx,
                "text_snippet": p.text[:120]
            })
            warnings.append(f"Phát hiện nhãn cần xác minh [NEEDS_VERIFICATION] tại đoạn {idx}: '{p.text[:60]}...'")

    # Xác định kiểu trích dẫn chính
    is_apa = len(apa_in_text) > 0
    is_ieee = len(ieee_in_text) > 0
    
    citation_style = "APA" if is_apa and not is_ieee else ("IEEE" if is_ieee and not is_apa else ("MIXED" if is_apa and is_ieee else "UNKNOWN"))

    if citation_style == "MIXED":
        warnings.append("Cảnh báo phong cách trích dẫn hỗn hợp: Phát hiện cả trích dẫn APA và IEEE trong cùng tài liệu.")

    if not ref_entries:
        errors.append("Không tìm thấy mục Tài liệu tham khảo hoặc danh mục tham khảo rỗng.")
        return {
            "status": "FAIL",
            "file": docx_path,
            "citation_style": citation_style,
            "errors": errors,
            "warnings": warnings,
            "unreferenced_in_text": [c["raw"] for c in apa_in_text],
            "orphan_references": []
        }

    # 1. So khớp APA
    unreferenced_in_text = []
    orphan_references = []

    if is_apa or citation_style == "APA":
        matched_ref_indices = set()

        for cit in apa_in_text:
            author_clean = clean_author_for_matching(cit["author"])
            year = cit["year"]
            
            # Tìm trong danh mục tham khảo
            matched = False
            for idx, entry in enumerate(ref_entries):
                entry_clean = clean_author_for_matching(entry["author_part"])
                entry_year = entry["year"]
                
                # Khớp năm (nếu có) và ít nhất 1 token họ tên tác giả
                year_match = (year == entry_year) or (year in ["n.d.", "k.n."] and entry_year in [None, "n.d.", "k.n."])
                
                # So khớp token tác giả
                author_tokens = author_clean.split()
                has_token_match = any(tok in entry_clean for tok in author_tokens if len(tok) >= 2)
                
                if year_match and has_token_match:
                    matched = True
                    matched_ref_indices.add(idx)
                    break
            
            if not matched:
                unreferenced_in_text.append(cit["raw"])
                errors.append(f"Trích dẫn in-text không tìm thấy trong thư mục: '{cit['raw']}'")

        for idx, entry in enumerate(ref_entries):
            if idx not in matched_ref_indices:
                orphan_references.append(entry["raw_text"][:80])
                warnings.append(f"Tài liệu tham khảo chưa được trích dẫn trong bài (Orphan): '{entry['raw_text'][:70]}...'")

    # 2. So khớp IEEE
    if is_ieee:
        ref_ieee_nums = {e["ieee_num"] for e in ref_entries if e["ieee_num"] is not None}
        for num in ieee_in_text:
            if num not in ref_ieee_nums:
                unreferenced_in_text.append(f"[{num}]")
                errors.append(f"Số trích dẫn IEEE [{num}] không có trong danh mục tham khảo.")
        for num in ref_ieee_nums:
            if num not in ieee_in_text:
                warnings.append(f"Tài liệu IEEE [{num}] trong thư mục chưa được trích dẫn trong bài.")

    status = "FAIL" if errors else ("WARNING" if warnings else "PASS")

    return {
        "status": status,
        "file": docx_path,
        "citation_style": citation_style,
        "in_text_count": len(apa_in_text) + len(ieee_in_text),
        "reference_entries_count": len(ref_entries),
        "unreferenced_in_text": list(set(unreferenced_in_text)),
        "orphan_references": orphan_references,
        "unverified_flags": unverified_flags,
        "errors": errors,
        "warnings": warnings,
        "disclaimer": "Kiểm tra tính nhất quán văn bản (Textual Citation Consistency). Chưa xác minh tính chân thực thực tế của nguồn nếu chưa tra cứu CSDL ngoài."
    }


def main():
    parser = argparse.ArgumentParser(description="Kiểm tra tính nhất quán hệ thống trích dẫn APA 7 và IEEE trong DOCX.")
    parser.add_argument("--file", "-f", required=True, help="Đường dẫn tới file DOCX cần kiểm tra.")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON.")
    args = parser.parse_args()

    result = validate_citations(args.file)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n" + "="*60)
        print(f"KẾT QUẢ KIỂM TRA TRÍCH DẪN: {result['status']}")
        print(f"Tập tin: {result['file']}")
        print(f"Phong cách trích dẫn phát hiện: {result.get('citation_style', 'UNKNOWN')}")
        print("="*60)
        print(f"Số trích dẫn in-text: {result.get('in_text_count', 0)}")
        print(f"Số mục trong danh mục tham khảo: {result.get('reference_entries_count', 0)}")

        if result.get("unreferenced_in_text"):
            print(f"\n[LỖI] Trích dẫn mồ côi ngược (Trong bài có, Thư mục KHÔNG):")
            for cit in result["unreferenced_in_text"]:
                print(f"  - {cit}")

        if result.get("orphan_references"):
            print(f"\n[CẢNH BÁO] Tài liệu mồ côi xuôi (Thư mục có, Trong bài CHƯA viện dẫn):")
            for ref in result["orphan_references"]:
                print(f"  - {ref}")

        if result.get("unverified_flags"):
            print(f"\n[CẢNH BÁO] Các vị trí gắn nhãn [NEEDS_VERIFICATION]: {len(result['unverified_flags'])}")

        print("\n* Ghi chú:", result.get("disclaimer", ""))
        print("="*60 + "\n")

    sys.exit(0 if result["status"] in ["PASS", "WARNING"] else 1)


if __name__ == "__main__":
    main()
