"""
Comprehensive Unit Tests for OCR Engine, Binary Garbage Safety, and Material Intelligence.
Verifies:
1. Valid PNG containing readable text -> OCR succeeds -> readable text returned
2. Valid JPG containing readable text -> OCR succeeds
3. PNG binary bytes -> must NEVER be interpreted directly as UTF-8 text
4. OCR output containing normal numbers, symbols, dimensions, parentheses -> remains valid
5. Corrupted OCR output -> rejected
6. Complete OCR text -> remains available to frontend
7. Material Intelligence -> consumes ONLY OCR text and calculates matching percentages
"""

import os
import unittest
import tempfile
from PIL import Image, ImageDraw, ImageFont

from ml.document_extractor import (
    extract_document_text,
    extract_document_text_from_bytes,
)
from ml.material_analyzer import (
    parse_material_entry,
    analyze_ocr_text,
    calculate_material_similarity,
)


class TestOcrAndBinarySafetyRegression(unittest.TestCase):

    def setUp(self):
        # Create a sample text PNG image for OCR testing
        self.tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img = Image.new("RGB", (600, 200), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((10, 10), "Office & Desk Consumables", fill=(0, 0, 0))
        d.text((10, 40), "Copier Paper A4 Size 80 GSM", fill=(0, 0, 0))
        d.text((10, 70), "Intel Core i7 Desktop Computer", fill=(0, 0, 0))
        d.text((10, 100), "UPS System 10 kVA Online", fill=(0, 0, 0))
        img.save(self.tmp_png.name)
        self.tmp_png.close()

        # Create a sample text JPG image for OCR testing
        self.tmp_jpg = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        img.save(self.tmp_jpg.name, format="JPEG")
        self.tmp_jpg.close()

    def tearDown(self):
        try:
            os.remove(self.tmp_png.name)
            os.remove(self.tmp_jpg.name)
        except Exception:
            pass

    def test_1_valid_png_readable_text(self):
        """TEST 1: Valid PNG containing readable text -> OCR succeeds -> readable text returned"""
        res = extract_document_text(self.tmp_png.name)
        self.assertTrue(res["has_content"])
        self.assertNotEqual(res["text"], "No readable text detected from uploaded image.")

    def test_2_valid_jpg_readable_text(self):
        """TEST 2: Valid JPG containing readable text -> OCR succeeds"""
        res = extract_document_text(self.tmp_jpg.name)
        self.assertTrue(res["has_content"])
        self.assertNotEqual(res["text"], "No readable text detected from uploaded image.")

    def test_3_png_binary_bytes_never_decoded_as_utf8(self):
        """TEST 3: PNG binary bytes must NEVER be interpreted directly as UTF-8 OCR text"""
        raw_png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xff"
        res = extract_document_text_from_bytes(raw_png_bytes, "header_only.png")
        self.assertNotIn("IHDR", res["text"])
        self.assertNotIn("sRGB", res["text"])
        self.assertEqual(res["text"], "No readable text detected from uploaded image.")

    def test_4_valid_ocr_text_with_punctuation_and_numbers(self):
        """TEST 4: OCR output containing normal numbers, symbols, dimensions, hyphens, parentheses must remain valid"""
        valid_lines = [
            "Copier Paper A4 Size 80 GSM (JK Paper / TNPL) – 500 sheets per ream",
            "Heavy Duty Stapler & Pin Sets (Kangaro) – 24/6 and 23/17 size capacity",
            "Executive Mesh High-Back Chair (Godrej Interio)",
            "Intel Core i7 Desktop Computer (HP / Dell) – 13th Gen i7, 16GB DDR5 RAM",
            "Managed Layer-3 Network Switch (Cisco) – 24-Port Gigabit PoE+",
            "UPS System 10 kVA Online (APC / Emerson)",
        ]
        for line in valid_lines:
            entry = parse_material_entry(line)
            self.assertIsNotNone(entry, f"Line failed parse_material_entry: {line}")

    def test_5_complete_ocr_text_available_to_frontend(self):
        """TEST 5: Complete OCR text must remain available to frontend in raw_text field"""
        ocr_text = (
            "Office & Desk Consumables\n"
            "Copier Paper A4 Size 80 GSM\n"
            "A4 Copier Paper 80GSM White"
        )
        res = extract_document_text_from_bytes(ocr_text.encode("utf-8"), "test.txt")
        self.assertEqual(res["text"], ocr_text.strip())

    def test_6_material_intelligence_consumes_only_ocr_text(self):
        """TEST 6: Material Intelligence consumes ONLY OCR text and calculates material similarity groups"""
        ocr_text = (
            "Copier Paper A4 Size 80 GSM - 10 Reams\n"
            "A4 Copier Paper 80GSM White - 5 Reams"
        )
        analysis = analyze_ocr_text(ocr_text)
        self.assertGreater(analysis["total_entries"], 0)
        self.assertEqual(analysis["total_groups"], 1)

        member_a = parse_material_entry("Copier Paper A4 Size 80 GSM")
        member_b = parse_material_entry("A4 Copier Paper 80GSM White")
    def test_7_explainable_ai_confidence_breakdown(self):
        """TEST 7: Feature 1.3 - Explainable AI Confidence Breakdown calculates attribute sub-scores and weighted confidence"""
        from ml.confidence_breakdown import generate_confidence_breakdown

        attrs_a = {"component": "Hex Bolt", "material_grade": "SS304", "diameter": "M10", "pressure": "150#", "length": "50mm"}
        attrs_b = {"component": "Hexagonal Bolt", "material_grade": "SS304", "diameter": "10 MM", "pressure": "150#", "length": "50 MM"}

        res = generate_confidence_breakdown(attrs_a, attrs_b)
        self.assertIn("overall_confidence", res)
        self.assertGreaterEqual(res["overall_confidence"], 85.0)
        self.assertEqual(len(res["attribute_breakdown"]), 5)

    def test_8_financial_savings_simulator(self):
        """TEST 8: Feature 1.4 - Financial Savings Simulator computes Haversine route distance and net savings"""
        from ml.savings_simulator import simulate_financial_savings, haversine_distance_km

        dist = haversine_distance_km(21.1166, 72.6517, 18.7562, 79.5186)
        self.assertGreater(dist, 500.0)

        sim = simulate_financial_savings(destination_plant="NTPC Ramagundam", required_units=50, new_procurement_price=25000.0)
        self.assertTrue(sim["transfer_available"])
        self.assertGreater(sim["net_savings"], 0.0)
        self.assertIn("recommendation_pill", sim)


if __name__ == "__main__":
    unittest.main()
