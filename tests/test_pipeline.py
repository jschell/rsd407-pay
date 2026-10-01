import hashlib
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from rsd407_pay.pipeline import normalize_source, summarize


class PipelineTests(unittest.TestCase):
    def test_extracts_only_riverview_and_preserves_provenance(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "s275.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.title = "Districts Q-Z"
            ws.append(["School District", "Duty Title", "Cert FTE", "Clas FTE", "Base Salary", "Total Salary"])
            ws.append(["Other School District", "Teacher", 1, 0, 90000, 95000])
            ws.append(["Riverview", "Teacher", 1, 0, 100000, 105000])
            wb.save(path)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            rows = list(normalize_source({"school_year": "2024-25", "sha256": digest, "local_path": str(path)}))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["district_name"], "Riverview")
            self.assertEqual(rows[0]["source_sha256"], digest)
            self.assertEqual(rows[0]["source_sheet"], "Districts Q-Z")
            self.assertEqual(rows[0]["source_row"], 3)

    def test_rejects_raw_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "s275.xlsx"
            path.write_bytes(b"not the recorded source")
            with self.assertRaisesRegex(RuntimeError, "hash does not match"):
                list(normalize_source({"school_year": "2024-25", "sha256": "bad", "local_path": str(path)}))

    def test_summary_keeps_salary_and_fte_separate(self):
        rows = [
            {"school_year": "2024-25", "certificated_fte": 1.0, "classified_fte": 0.0, "base_salary": 100.0, "total_salary": 120.0},
            {"school_year": "2024-25", "certificated_fte": 0.0, "classified_fte": 0.5, "base_salary": 50.0, "total_salary": 60.0},
        ]
        item = summarize(rows)["2024-25"]
        self.assertEqual(item["rows"], 2)
        self.assertEqual(item["certificated_fte"], 1.0)
        self.assertEqual(item["classified_fte"], 0.5)
        self.assertEqual(item["base_salary"], 150.0)
        self.assertEqual(item["total_salary"], 180.0)


if __name__ == "__main__":
    unittest.main()
