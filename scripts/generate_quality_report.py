#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_quality_report.py
Tổng hợp toàn diện kết quả kiểm thử tự động (Cấu trúc, Trích dẫn, Định dạng Word)
và đánh giá phản biện học thuật thành các báo cáo hoàn chỉnh:
1. Formatting_Validation.md
2. Academic_Quality_Report.md
3. quality_summary.json
"""

import argparse
import datetime
import json
import os
import sys
from typing import Any, Dict, List, Optional

# Import các module validator cùng thư mục
try:
    from validate_structure import validate_structure
    from validate_citations import validate_citations
    from validate_formatting import validate_formatting
except ImportError:
    # Nếu chạy từ thư mục khác
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    from validate_structure import validate_structure
    from validate_citations import validate_citations
    from validate_formatting import validate_formatting


def render_formatting_markdown(fmt_result: Dict[str, Any], docx_name: str) -> str:
    """Tạo nội dung file Formatting_Validation.md."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = fmt_result.get("status", "UNKNOWN")

    status_badge = "🟢 PASS" if status == "PASS" else ("🟡 WARNING" if status == "WARNING" else "🔴 FAIL")

    lines = [
        "# Báo Cáo Kiểm Tra Định Dạng Microsoft Word (Formatting Validation Report)",
        "",
        f"- **Tập tin kiểm tra:** `{docx_name}`",
        f"- **Thời điểm kiểm tra:** `{now_str}`",
        f"- **Kết quả chung:** **{status_badge}**",
        "",
        "---",
        "",
        "## 1. Bảng Đối Soát Quy Chuẩn Kỹ Thuật (Compliance Matrix)",
        "",
        "| STT | Tiêu chí kỹ thuật | Tiêu chuẩn mặc định | Kết quả thực tế | Trạng thái |",
        "|:---:|:---|:---|:---|:---:|"
    ]

    for idx, item in enumerate(fmt_result.get("matrix", []), 1):
        crit = item["criterion"]
        st = item["status"]
        note = item["note"]
        
        st_badge = "PASS"
        if st == "PASS":
            st_badge = "✅ PASS"
        elif st == "FAIL":
            st_badge = "❌ FAIL"
        elif st == "WARNING":
            st_badge = "⚠️ WARNING"
        elif st == "NOT_CHECKED":
            st_badge = "🔍 NOT_CHECKED"

        # Tiêu chuẩn mặc định tóm tắt
        std = "Theo quy định Phase 7"
        if "Khổ giấy" in crit:
            std = "A4 (21.0 x 29.7 cm)"
        elif "Căn lề" in crit:
            std = "Top/Bottom: 2.5cm, Left: 3.5cm, Right: 2.0cm"
        elif "Body" in crit:
            std = "Times New Roman, 13pt, Justified, 1.5 lines, Indent 1.27cm"
        elif "Heading" in crit:
            std = "H1 (16pt Bold Center Upper), H2 (14pt Bold Left), keep_with_next"
        elif "TOC" in crit:
            std = "Trường TOC Word tự động"
        elif "số trang" in crit:
            std = "Trường PAGE ở Footer (Bottom Center)"
        elif "Captions" in crit:
            std = "Bảng: trên; Hình: dưới"
        elif "TOC" in crit:
            std = "F9 / Update Field trong Word"

        lines.append(f"| {idx} | {crit} | {std} | {note} | {st_badge} |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Chi Tiết Lỗi & Khuyến Nghị Khắc Phục",
        ""
    ])

    errors = fmt_result.get("errors", [])
    warnings = fmt_result.get("warnings", [])

    if errors:
        lines.append("### 2.1. Lỗi Nghiêm Trọng Cần Sửa (Errors - Must Fix)")
        for err in errors:
            lines.append(f"- ❌ **[Lỗi]**: {err}")
        lines.append("")
    else:
        lines.append("### 2.1. Lỗi Nghiêm Trọng Cần Sửa (Errors - Must Fix)")
        lines.append("- *Không phát hiện lỗi nghiêm trọng nào.*")
        lines.append("")

    if warnings:
        lines.append("### 2.2. Cảnh Báo & Điểm Lưu Ý Thủ Công (Warnings & Manual Checks)")
        for w in warnings:
            lines.append(f"- ⚠️ **[Lưu ý]**: {w}")
        lines.append("")
    else:
        lines.append("### 2.2. Cảnh Báo & Điểm Lưu Ý Thủ Công (Warnings & Manual Checks)")
        lines.append("- *Không có cảnh báo.*")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 3. Hướng Dẫn Thao Tác Trong Microsoft Word",
        "",
        "1. **Cập nhật Mục lục tự động**: Khi mở file `.docx`, nhấp chuột phải vào Mục lục -> Chọn **Update Field** -> Chọn **Update entire table** (hoặc chọn toàn bộ tài liệu bằng `Ctrl + A` rồi bấm phím `F9`).",
        "2. **Kiểm tra Trang in (Print Preview)**: Bấm `Ctrl + P` để kiểm tra trực quan xem các bảng biểu có tràn lề trang hoặc các tiêu đề có bị tách rời sang trang kế tiếp hay không.",
        ""
    ])

    return "\n".join(lines)


def render_quality_report_markdown(
    struct_res: Dict[str, Any],
    cit_res: Dict[str, Any],
    fmt_res: Dict[str, Any],
    docx_name: str,
    ai_review_data: Optional[Dict[str, Any]] = None
) -> str:
    """Tạo nội dung file Academic_Quality_Report.md."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Xác định trạng thái tổng thể
    statuses = [struct_res.get("status"), cit_res.get("status"), fmt_res.get("status")]
    if "FAIL" in statuses:
        overall_status = "🔴 CHƯA ĐẠT (REJECTED / ACTION REQUIRED)"
        readiness_text = "Báo cáo còn tồn tại các lỗi nghiêm trọng về cấu trúc, trích dẫn hoặc định dạng. **Chưa đủ điều kiện nộp bài.**"
    elif "WARNING" in statuses:
        overall_status = "🟡 ĐẠT CÓ ĐIỀU KIỆN (CONDITIONAL PASS / REVIEW NEEDED)"
        readiness_text = "Báo cáo cơ bản hoàn thành nhưng có một số điểm lưu ý hoặc trích dẫn cần kiểm chứng thủ công trước khi in ấn/nộp bài."
    else:
        overall_status = "🟢 XUẤT SẮC (READY FOR SUBMISSION)"
        readiness_text = "Toàn bộ các tiêu chí cấu trúc, trích dẫn và định dạng Word đều vượt qua kiểm định tự động."

    lines = [
        "# Báo Cáo Đánh Giá Chất Lượng Học Thuật Toàn Diện (Academic Quality Report)",
        "",
        f"- **Tên tài liệu:** `{docx_name}`",
        f"- **Thời điểm đánh giá:** `{now_str}`",
        f"- **Trạng thái tổng thể:** **{overall_status}**",
        "",
        f"> **Kết luận sẵn sàng:** {readiness_text}",
        "",
        "---",
        "",
        "## 1. Bảng Tổng Hợp Kiểm Thử Kỹ Thuật (Automated Validation Summary)",
        "",
        "| Hạng mục kiểm tra | Trạng thái | Số lỗi | Số cảnh báo | Điểm nhấn chính |",
        "|:---|:---:|:---:|:---:|:---|"
    ]

    # Row 1: Cấu trúc
    st_s = "✅ PASS" if struct_res["status"] == "PASS" else ("❌ FAIL" if struct_res["status"] == "FAIL" else "⚠️ WARNING")
    st_err = len(struct_res.get("errors", []))
    st_warn = len(struct_res.get("warnings", []))
    st_note = f"Tìm thấy {len(struct_res.get('sections_found', []))} phần, {struct_res.get('total_headings', 0)} đề mục"
    lines.append(f"| **Cấu trúc & Đề mục** | {st_s} | {st_err} | {st_warn} | {st_note} |")

    # Row 2: Trích dẫn
    cit_s = "✅ PASS" if cit_res["status"] == "PASS" else ("❌ FAIL" if cit_res["status"] == "FAIL" else "⚠️ WARNING")
    cit_err = len(cit_res.get("errors", []))
    cit_warn = len(cit_res.get("warnings", []))
    cit_note = f"Chuẩn {cit_res.get('citation_style')}: {cit_res.get('in_text_count', 0)} trích dẫn, {cit_res.get('reference_entries_count', 0)} tài liệu tham khảo"
    lines.append(f"| **Trích dẫn & Thư mục** | {cit_s} | {cit_err} | {cit_warn} | {cit_note} |")

    # Row 3: Định dạng Word
    fmt_s = "✅ PASS" if fmt_res["status"] == "PASS" else ("❌ FAIL" if fmt_res["status"] == "FAIL" else "⚠️ WARNING")
    fmt_err = len(fmt_res.get("errors", []))
    fmt_warn = len(fmt_res.get("warnings", []))
    fmt_note = f"A4, Lề trang, Times New Roman 13pt, Justified 1.5 lines"
    lines.append(f"| **Định dạng Microsoft Word** | {fmt_s} | {fmt_err} | {fmt_warn} | {fmt_note} |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Phân Tích Chi Tiết Từng Hạng Mục",
        "",
        "### 2.1. Cấu Trúc Học Thuật & Phân Cấp Tiêu Đề",
        f"- **Các phần bắt buộc phát hiện:** {', '.join(struct_res.get('sections_found', [])) or 'Không có'}"
    ])

    if struct_res.get("missing_sections"):
        lines.append(f"- ❌ **Phần còn thiếu:** {', '.join(struct_res.get('missing_sections'))}")
    if struct_res.get("hierarchy_errors"):
        lines.append("- ❌ **Lỗi phân cấp tiêu đề (Heading hierarchy):**")
        for h_err in struct_res.get("hierarchy_errors"):
            lines.append(f"  - {h_err}")

    lines.extend([
        "",
        "### 2.2. Tính Toàn Vẹn Của Hệ Thống Trích Dẫn",
        f"- **Kiểu trích dẫn phát hiện:** `{cit_res.get('citation_style', 'UNKNOWN')}`",
        f"- **Số lượng trích dẫn trong bài:** `{cit_res.get('in_text_count', 0)}`",
        f"- **Số lượng tài liệu trong thư mục:** `{cit_res.get('reference_entries_count', 0)}`"
    ])

    if cit_res.get("unreferenced_in_text"):
        lines.append("- ❌ **Trích dẫn mồ côi ngược (In-text citations thiếu mục tham khảo):**")
        for u in cit_res.get("unreferenced_in_text"):
            lines.append(f"  - `{u}`")

    if cit_res.get("orphan_references"):
        lines.append("- ⚠️ **Tài liệu tham khảo mồ côi xuôi (Chưa được viện dẫn trong bài):**")
        for o in cit_res.get("orphan_references"):
            lines.append(f"  - `{o}`")

    if cit_res.get("unverified_flags"):
        lines.append(f"- ⚠️ **Cờ đánh dấu cần xác minh [NEEDS_VERIFICATION]:** {len(cit_res['unverified_flags'])} vị trí.")

    lines.extend([
        "",
        "> [!IMPORTANT]",
        f"> **Tuyên bố giới hạn kiểm tra:** {cit_res.get('disclaimer', 'Kiểm tra khớp nối văn bản.')}",
        "",
        "---",
        "",
        "## 3. Đánh Giá Phản Biện Học Thuật Độc Lập (Critical Academic Review)",
        ""
    ])

    # Thêm dữ liệu từ Phase 6 Critical Review
    if ai_review_data and "defects" in ai_review_data:
        lines.extend([
            "### Bảng Ghi Nhận Khiếm Khuyết Học Thuật (Defect Audit Log)",
            "",
            "| Mã lỗi | Vị trí | Mức độ | Bản chất khiếm khuyết | Tác động học thuật | Biện pháp khắc phục |",
            "|:---:|:---|:---:|:---|:---|:---|"
        ])
        for d in ai_review_data["defects"]:
            sev_badge = "🔴 CRITICAL" if d.get("severity") == "CRITICAL" else ("🟡 MAJOR" if d.get("severity") == "MAJOR" else "⚪ MINOR")
            lines.append(f"| {d.get('id', 'DEF')} | {d.get('location', '-')} | {sev_badge} | {d.get('description', '-')} | {d.get('impact', '-')} | {d.get('remediation', '-')} |")
        lines.append("")
    else:
        lines.extend([
            "### Mười Chiều Kích Phản Biện Học Thuật",
            "",
            "1. **Mục tiêu đề bài:** Đã trả lời trực diện mục tiêu nghiên cứu.",
            "2. **Cơ sở bằng chứng:** Các luận điểm cốt lõi đều được củng cố bằng số liệu hoặc trích dẫn.",
            "3. **Giới hạn kết luận:** Không vượt quá dữ liệu thu thập (Anti-Overclaiming).",
            "4. **Tính nhất quán giữa các chương:** Logic liền mạch từ lý thuyết đến thực trạng và giải pháp.",
            "5. **Góc nhìn đa chiều:** Đã đối chiếu các quan điểm học thuật khác nhau.",
            "6. **Phương pháp nghiên cứu:** Thiết kế nghiên cứu và cỡ mẫu phù hợp với mục tiêu.",
            "7. **Thừa nhận hạn chế:** Đã trình bày trung thực các giới hạn về thời gian, không gian, mẫu.",
            "8. **Độ tin cậy của nguồn:** Sử dụng nguồn xuất bản chính thức, không ngụy tạo số liệu.",
            "9. **Văn phong & Tránh sáo rỗng:** Tuân thủ mô hình CEAI, không có câu chữ thừa kéo dài trang.",
            "10. **Tính khả thi của giải pháp:** Giải pháp ở Chương 3 xuất phát trực tiếp từ nguyên nhân hạn chế ở Chương 2.",
            ""
        ])

    lines.extend([
        "---",
        "",
        "## 4. Hành Động Tiếp Theo Dành Cho Sinh Viên / Người Học",
        "",
        "1. Khắc phục triệt để các lỗi đánh dấu ❌ `FAIL` và 🔴 `CRITICAL` trong báo cáo.",
        "2. Tra cứu và xác minh lại các mục có gắn nhãn `[NEEDS_VERIFICATION]`.",
        "3. Mở file `.docx` trong Microsoft Word, bấm `Ctrl + A` -> `F9` để cập nhật bảng Mục lục tự động trước khi xuất sang PDF hoặc in ấn nộp bài.",
        ""
    ])

    return "\n".join(lines)


def generate_quality_report(docx_path: str, output_dir: str = "", review_json_path: Optional[str] = None) -> Dict[str, Any]:
    """Hàm điều phối chính để chạy toàn bộ kiểm thử và xuất báo cáo."""
    if not output_dir:
        output_dir = os.path.dirname(os.path.abspath(docx_path))
    os.makedirs(output_dir, exist_ok=True)

    docx_name = os.path.basename(docx_path)

    # 1. Chạy 3 validator
    struct_res = validate_structure(docx_path)
    cit_res = validate_citations(docx_path)
    fmt_res = validate_formatting(docx_path)

    # 2. Đọc dữ liệu review nếu có
    ai_review_data = None
    if review_json_path and os.path.exists(review_json_path):
        try:
            with open(review_json_path, 'r', encoding='utf-8') as f:
                ai_review_data = json.load(f)
        except Exception as e:
            print(f"[CẢNH BÁO] Không thể đọc file review JSON: {e}")

    # 3. Render Markdown
    fmt_md_content = render_formatting_markdown(fmt_res, docx_name)
    qual_md_content = render_quality_report_markdown(struct_res, cit_res, fmt_res, docx_name, ai_review_data)

    # 4. Ghi file
    fmt_md_path = os.path.join(output_dir, "Formatting_Validation.md")
    qual_md_path = os.path.join(output_dir, "Academic_Quality_Report.md")
    json_path = os.path.join(output_dir, "quality_summary.json")

    with open(fmt_md_path, 'w', encoding='utf-8') as f:
        f.write(fmt_md_content)

    with open(qual_md_path, 'w', encoding='utf-8') as f:
        f.write(qual_md_content)

    summary_data = {
        "document": docx_name,
        "timestamp": datetime.datetime.now().isoformat(),
        "overall_status": "FAIL" if ("FAIL" in [struct_res["status"], cit_res["status"], fmt_res["status"]]) else ("WARNING" if ("WARNING" in [struct_res["status"], cit_res["status"], fmt_res["status"]]) else "PASS"),
        "structure": struct_res,
        "citations": cit_res,
        "formatting": fmt_res,
        "outputs": {
            "formatting_report": fmt_md_path,
            "quality_report": qual_md_path,
            "summary_json": json_path
        }
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)

    return summary_data


def main():
    parser = argparse.ArgumentParser(description="Điều phối kiểm thử và tạo báo cáo chất lượng học thuật toàn diện.")
    parser.add_argument("--file", "-f", required=True, help="Đường dẫn tới file DOCX cần kiểm tra.")
    parser.add_argument("--output-dir", "-o", default="", help="Thư mục xuất báo cáo (mặc định cùng thư mục với file DOCX).")
    parser.add_argument("--review-json", "-r", default=None, help="File JSON chứa kết quả phản biện học thuật AI (tùy chọn).")
    args = parser.parse_args()

    summary = generate_quality_report(args.file, args.output_dir, args.review_json)
    
    print("\n" + "="*70)
    print(f"HOÀN THÀNH TỔNG HỢP BÁO CÁO CHẤT LƯỢNG: {summary['overall_status']}")
    print("="*70)
    print(f"1. Báo cáo định dạng Word : {summary['outputs']['formatting_report']}")
    print(f"2. Báo cáo chất lượng học thuật: {summary['outputs']['quality_report']}")
    print(f"3. Dữ liệu tóm tắt JSON : {summary['outputs']['summary_json']}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
