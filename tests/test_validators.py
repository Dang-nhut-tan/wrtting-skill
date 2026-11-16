#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_validators.py
Bộ kiểm thử tự động (Unit / Integration Tests) cho các scripts kiểm định chất lượng:
- test_structure_validation
- test_citation_validation
- test_formatting_validation
- test_quality_report_generation
"""

import json
import os
import sys
import unittest

# Thêm đường dẫn thư mục scripts vào sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
TESTS_DIR = os.path.join(BASE_DIR, "tests")
sys.path.insert(0, SCRIPTS_DIR)

from validate_structure import validate_structure
from validate_citations import validate_citations
from validate_formatting import validate_formatting
from generate_quality_report import generate_quality_report


class TestAcademicReportValidators(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.valid_docx = os.path.join(TESTS_DIR, "sample_report_valid.docx")
        cls.error_docx = os.path.join(TESTS_DIR, "sample_report_with_errors.docx")
        
        assert os.path.exists(cls.valid_docx), f"Không tìm thấy {cls.valid_docx}"
        assert os.path.exists(cls.error_docx), f"Không tìm thấy {cls.error_docx}"

    def test_01_structure_valid_document(self):
        """Kiểm tra cấu trúc trên tài liệu chuẩn -> Phải đạt PASS hoặc chỉ WARNING nhẹ."""
        res = validate_structure(self.valid_docx)
        self.assertIn(res["status"], ["PASS", "WARNING"])
        self.assertIn("Mở đầu", res["sections_found"])
        self.assertIn("Kết luận", res["sections_found"])
        self.assertIn("Tài liệu tham khảo", res["sections_found"])
        self.assertEqual(len(res["missing_sections"]), 0)
        self.assertEqual(len(res["hierarchy_errors"]), 0)

    def test_02_structure_error_document(self):
        """Kiểm tra cấu trúc trên tài liệu chứa lỗi -> Phải báo FAIL với đúng lỗi thiếu Kết luận và nhảy cóc cấp độ."""
        res = validate_structure(self.error_docx)
        self.assertEqual(res["status"], "FAIL")
        # Phải phát hiện thiếu Kết luận
        self.assertIn("Kết luận", res["missing_sections"])
        # Phải phát hiện lỗi nhảy cóc cấp đề mục (H1 -> H3)
        self.assertTrue(len(res["hierarchy_errors"]) > 0, "Không phát hiện lỗi nhảy cóc cấp đề mục.")
        # Phải phát hiện thứ tự chương không liên tục (1 rồi đến 3)
        self.assertTrue(any("Thứ tự số hiệu chương" in err for err in res["errors"]))

    def test_03_citations_valid_document(self):
        """Kiểm tra trích dẫn trên tài liệu chuẩn -> Khớp 100% hai chiều giữa in-text và thư mục."""
        res = validate_citations(self.valid_docx)
        self.assertIn(res["status"], ["PASS", "WARNING"])
        self.assertEqual(len(res["unreferenced_in_text"]), 0, f"Có trích dẫn mồ côi ngoài ý muốn: {res['unreferenced_in_text']}")
        self.assertEqual(res["citation_style"], "APA")

    def test_04_citations_error_document(self):
        """Kiểm tra trích dẫn trên tài liệu lỗi -> Bắt đúng trích dẫn mồ côi, tài liệu mồ côi và cờ NEEDS_VERIFICATION."""
        res = validate_citations(self.error_docx)
        self.assertEqual(res["status"], "FAIL")
        
        # Phải phát hiện trích dẫn mồ côi (Lê Văn C hoặc Smith)
        unreferenced_str = " ".join(res["unreferenced_in_text"])
        self.assertTrue("Lê Văn C" in unreferenced_str or "Smith" in unreferenced_str, 
                        f"Không bắt được trích dẫn mồ côi Lê Văn C / Smith: {res['unreferenced_in_text']}")
        
        # Phải phát hiện tài liệu mồ côi trong thư mục (Vũ, 2022)
        orphan_str = " ".join(res["orphan_references"])
        self.assertTrue("Vũ" in orphan_str, f"Không bắt được tài liệu mồ côi Vũ (2022): {res['orphan_references']}")
        
        # Phải phát hiện cờ NEEDS_VERIFICATION
        self.assertTrue(len(res["unverified_flags"]) > 0, "Không bắt được nhãn NEEDS_VERIFICATION")

    def test_05_formatting_valid_document(self):
        """Kiểm tra định dạng Word trên tài liệu chuẩn -> A4, margins, Heading styles đều đạt chuẩn."""
        res = validate_formatting(self.valid_docx)
        self.assertIn(res["status"], ["PASS", "WARNING"])
        self.assertTrue(res["page_setup"]["is_a4"], "Không nhận diện đúng khổ A4")
        self.assertEqual(len(res["page_setup"]["margin_issues"]), 0, f"Lỗi lề trang không mong muốn: {res['page_setup']['margin_issues']}")
        self.assertTrue(res["fields_check"]["has_page_number_field"], "Thiếu mã số trang PAGE")
        self.assertTrue(res["fields_check"]["has_toc_field"], "Thiếu mã mục lục TOC")

    def test_06_formatting_error_document(self):
        """Kiểm tra định dạng Word trên tài liệu lỗi -> Bắt đúng lỗi lề trang sai, thiếu số trang, dòng trống liên tiếp."""
        res = validate_formatting(self.error_docx)
        self.assertEqual(res["status"], "FAIL")
        
        # Phải bắt lỗi lề trang
        self.assertTrue(len(res["page_setup"]["margin_issues"]) > 0, "Không bắt được lỗi căn lề trang")
        
        # Phải bắt thiếu trường số trang
        self.assertFalse(res["fields_check"]["has_page_number_field"], "Không phát hiện thiếu số trang footer")
        
        # Phải bắt lạm dụng dòng trống liên tiếp (>2)
        self.assertGreater(res["body_check"]["max_consecutive_empty"], 2, "Không phát hiện lạm dụng dòng trống")

    def test_07_generate_quality_report(self):
        """Kiểm tra tính năng tổng hợp báo cáo chất lượng ra file Markdown và JSON."""
        out_dir = os.path.join(TESTS_DIR, "output_test")
        
        # Chạy trên tài liệu có lỗi
        res_error = generate_quality_report(self.error_docx, output_dir=out_dir)
        self.assertEqual(res_error["overall_status"], "FAIL")
        self.assertTrue(os.path.exists(res_error["outputs"]["formatting_report"]))
        self.assertTrue(os.path.exists(res_error["outputs"]["quality_report"]))
        self.assertTrue(os.path.exists(res_error["outputs"]["summary_json"]))

        # Kiểm tra nội dung file sinh ra
        with open(res_error["outputs"]["quality_report"], 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("CHƯA ĐẠT", content)
            self.assertIn("Lê Văn C", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
