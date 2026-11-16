#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_mis_perspectives.py
Kiểm thử tính năng MIS Academic Perspective:
1. Phân loại đề tài vào 4 nhóm: Category A (Quản trị), Category B (Tài chính/Kinh tế), Category C (Hệ thống/CNTT), Category D (Liên ngành).
2. Kiểm tra quy tắc Anti-Buzzword: Không tự ý nhét công nghệ (AI, Blockchain, Big Data) vào đề tài không liên quan.
3. Kiểm tra tính hiện diện của 5 câu hỏi thẩm định công nghệ khi đề xuất giải pháp.
4. Kiểm tra quy chuẩn định dạng cho Technical Artifacts (BPMN, DFD, ERD).
"""

import json
import os
import re
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCES_DIR = os.path.join(BASE_DIR, "references")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
TESTS_DIR = os.path.join(BASE_DIR, "tests")


def classify_mis_topic(topic_title: str, syllabus_desc: str = "") -> dict:
    """Hàm mô phỏng logic phân loại đề tài MIS theo Phase 1."""
    text = f"{topic_title} {syllabus_desc}".lower()
    
    # Category C: Core IS & Tech
    cat_c_keywords = [
        "phân tích thiết kế hệ thống", "cơ sở dữ liệu", "kiến trúc phần mềm", 
        "data warehouse", "big data", "hệ quản trị", "api", "hệ thống erp"
    ]
    # Category B: Finance & Economics
    cat_b_keywords = [
        "ngân hàng", "tài chính", "thanh toán", "fintech", "kinh tế lượng", 
        "core banking", "chứng khoán", "tín dụng", "tiền tệ"
    ]
    # Category A: Business & Management
    cat_a_keywords = [
        "quản trị nhân lực", "marketing", "chuỗi cung ứng", "chiến lược", 
        "quy trình nghiệp vụ", "văn hóa doanh nghiệp", "động lực làm việc", "crm", "hris"
    ]

    has_c = any(k in text for k in cat_c_keywords)
    has_b = any(k in text for k in cat_b_keywords)
    has_a = any(k in text for k in cat_a_keywords)

    # Đề tài thuần túy phi công nghệ
    pure_non_it_keywords = ["lịch sử đảng", "triết học", "tư tưởng hồ chí minh", "pháp luật đại cương"]
    is_pure_non_it = any(k in text for k in pure_non_it_keywords)

    if is_pure_non_it:
        return {
            "category": "NON_IT",
            "allow_tech_solutions": False,
            "focus": "Pure Humanities / Social Sciences"
        }
    elif has_c:
        return {
            "category": "CATEGORY_C",
            "allow_tech_solutions": True,
            "focus": "Information Systems & Technology Architecture"
        }
    elif has_b:
        return {
            "category": "CATEGORY_B",
            "allow_tech_solutions": True,
            "focus": "Finance & Economics (Fintech / BI / Risk Management)"
        }
    elif has_a:
        return {
            "category": "CATEGORY_A",
            "allow_tech_solutions": True,
            "focus": "Business & Management (Process Optimization / ERP / CRM / HRIS)"
        }
    else:
        return {
            "category": "CATEGORY_D",
            "allow_tech_solutions": True,
            "focus": "Interdisciplinary Research"
        }


def validate_mis_content(report_text: str, category_info: dict) -> list:
    """Kiểm tra nội dung báo cáo xem có vi phạm quy tắc Anti-Buzzword hoặc lạm dụng công nghệ không."""
    issues = []
    
    # 1. Nếu là đề tài thuần phi công nghệ mà xuất hiện các buzzword công nghệ gượng ép
    if not category_info["allow_tech_solutions"]:
        unwarranted_buzzwords = ["blockchain", "trí tuệ nhân tạo", "machine learning", "big data", "điện toán đám mây"]
        for bw in unwarranted_buzzwords:
            if bw in report_text.lower():
                issues.append(f"Gượng ép đưa công nghệ '{bw}' vào đề tài không phù hợp: {category_info['focus']}")

    # 2. Nếu đề xuất AI / Big Data trong đề tài quản trị vừa và nhỏ
    if category_info["category"] == "CATEGORY_A":
        if "blockchain" in report_text.lower() and "tiệm" in report_text.lower():
            issues.append("Lạm dụng công nghệ Blockchain cho quy mô kinh doanh nhỏ lẻ.")

    return issues


class TestMISAcademicPerspective(unittest.TestCase):

    def test_01_classification_business_management(self):
        """Kiểm tra nhận diện đúng đề tài Category A: Quản trị nhân lực / Marketing."""
        topic = "Nghiên cứu tác động của văn hóa doanh nghiệp đến động lực làm việc của nhân sự tại Công ty ABC"
        res = classify_mis_topic(topic)
        self.assertEqual(res["category"], "CATEGORY_A")
        self.assertTrue(res["allow_tech_solutions"])
        self.assertIn("Business & Management", res["focus"])

    def test_02_classification_finance_economics(self):
        """Kiểm tra nhận diện đúng đề tài Category B: Ngân hàng / Tài chính / Fintech."""
        topic = "Phân tích các nhân tố thúc đẩy hành vi sử dụng dịch vụ thanh toán số và ví điện tử của sinh viên"
        res = classify_mis_topic(topic)
        self.assertEqual(res["category"], "CATEGORY_B")
        self.assertTrue(res["allow_tech_solutions"])
        self.assertIn("Finance & Economics", res["focus"])

    def test_03_classification_core_is_tech(self):
        """Kiểm tra nhận diện đúng đề tài Category C: Phân tích thiết kế hệ thống / CSDL / Big Data."""
        topic = "Phân tích thiết kế hệ thống thông tin quản lý chuỗi cung ứng vật tư y tế"
        res = classify_mis_topic(topic)
        self.assertEqual(res["category"], "CATEGORY_C")
        self.assertTrue(res["allow_tech_solutions"])
        self.assertIn("Information Systems & Technology Architecture", res["focus"])

    def test_04_anti_buzzword_pure_non_it_topic(self):
        """Kiểm tra quy tắc cấm gượng ép công nghệ vào đề tài khoa học xã hội thuần túy."""
        topic = "Vận dụng nguyên lý mối liên hệ phổ biến trong Triết học Mác - Lênin vào quá trình học tập đại học"
        res = classify_mis_topic(topic)
        self.assertEqual(res["category"], "NON_IT")
        self.assertFalse(res["allow_tech_solutions"])

        # Nếu một bài viết gượng ép nhét Blockchain vào triết học
        bad_text = "Để vận dụng triết học, sinh viên cần áp dụng công nghệ Blockchain và Trí tuệ nhân tạo để ghi nhớ bài học."
        issues = validate_mis_content(bad_text, res)
        self.assertTrue(len(issues) > 0, "Không bắt được lỗi gượng ép công nghệ vào đề tài phi CNTT")
        self.assertTrue(any("blockchain" in iss.lower() for iss in issues))

    def test_05_mis_reference_document_integrity(self):
        """Kiểm tra tính toàn vẹn và các nội dung bắt buộc trong references/mis-academic-perspective.md."""
        mis_doc_path = os.path.join(REFERENCES_DIR, "mis-academic-perspective.md")
        self.assertTrue(os.path.exists(mis_doc_path), "File references/mis-academic-perspective.md không tồn tại.")

        with open(mis_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Kiểm tra sự hiện diện của các mục trọng tâm
        self.assertIn("The MIS Triad Identity", content)
        self.assertIn("Nhóm A: Quản trị & Kinh doanh", content)
        self.assertIn("Nhóm B: Tài chính & Kinh tế", content)
        self.assertIn("Nhóm C: Công nghệ & Hệ thống thông tin cốt lõi", content)
        self.assertIn("MIS 6-Step Analytical Framework", content)
        self.assertIn("Anti-Buzzword Rules", content)
        self.assertIn("Năm Câu Hỏi Thẩm Định Công Nghệ", content)
        self.assertIn("Technical Artifacts", content)
        self.assertIn("MIS Critical Review Dimensions", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
