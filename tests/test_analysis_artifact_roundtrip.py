"""Exercise report files across the same CLI boundary as retained analysis."""
import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from rsd407_pay import table45b_reconcile, personnel_compensation_compare, validation
from rsd407_pay import personnel_compensation, normalize_metrics, admin_overhead, findings

class AnalysisArtifactTests(unittest.TestCase):
    def invoke(self, main, args):
        with contextlib.redirect_stdout(io.StringIO()), patch("sys.argv", ["test", *args]):
            try:
                main(args)
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    raise

    def read_json(self, path):
        text = path.read_text()
        self.assertTrue(text.endswith("\n"))
        self.assertFalse(text.endswith(r"\n"))
        return json.loads(text)

    def test_report_files_roundtrip_through_validation_and_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            district = []
            categories = []
            rows = []
            enrollment = {"years": []}
            for i, year in enumerate(validation.YEARS):
                district.append({"school_year": year, "employee_rows": 3,
                    "total_fte": 3, "base_salary": 250, "total_salary": 300,
                    "insurance_benefits": 25, "mandatory_benefits": 50,
                    "reported_employer_compensation": 375})
                for family in ("district/central administration", "principals/APs"):
                    categories.append({"school_year": year, "job_family": family,
                        "total_fte": 1, "total_salary": 100,
                        "reported_employer_compensation": 125})
                rows.append({"school_year": year, "source_sha256": str(i),
                    "source_sheet": "S", "source_row": str(i+1),
                    "certificated_fte": 2, "classified_fte": 1,
                    "base_salary": 250, "total_salary": 300,
                    "insurance_benefits": 25, "mandatory_benefits": 50})
                enrollment["years"].append({"school_year": year,
                    "student_fte": 100, "measure": "annual_average"})
            metrics = {"district": district, "categories": categories}
            components = [
                {"total_fte": 2, "average_base_salary_per_fte": 100,
                 "average_total_salary_per_fte": 120,
                 "average_insurance_benefits_per_fte": 10,
                 "average_mandatory_benefits_per_fte": 20},
                {"total_fte": 1, "average_base_salary_per_fte": 50,
                 "average_total_salary_per_fte": 60,
                 "average_insurance_benefits_per_fte": 5,
                 "average_mandatory_benefits_per_fte": 10},
            ]
            controls = {"district_code": "17407", "years": [
                {"school_year": year, "source_sha256": year,
                 "table45b": {"total_fte": 3}, "compensation_rows": components}
                for year in validation.YEARS[-6:]]}
            cpi = {"series": {name: {"series_id": name, "geography": name,
                "values": {str(year): 100 for year in range(2014, 2026)}}
                for name in normalize_metrics.CPI}}
            for name, payload in (("metrics", metrics), ("controls", controls),
                                  ("enrollment", enrollment), ("cpi", cpi)):
                (root / (name+".json")).write_text(json.dumps(payload))
            csv_path = root / "rows.csv"
            with csv_path.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            fte_path, comp_path = root / "fte.json", root / "comp.json"
            common = ["--controls", str(root/"controls.json"),
                      "--metrics", str(root/"metrics.json")]
            self.invoke(table45b_reconcile.main, common+["--output", str(fte_path)])
            self.invoke(personnel_compensation_compare.main,
                        common+["--output", str(comp_path)])
            self.assertEqual(self.read_json(fte_path)["status"], "pass")
            self.assertEqual(self.read_json(comp_path)["base_salary_control_status"], "pass")
            report_path = root / "validation.json"
            args = ["--input", str(csv_path), "--metrics", str(root/"metrics.json"),
                    "--external-reconciliation", str(fte_path),
                    "--external-compensation", str(comp_path),
                    "--output", str(report_path)]
            self.invoke(validation.main, args)
            report = self.read_json(report_path)
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["external_reconciliation"]["checked_years"],
                             validation.YEARS[-6:])
            self.assertEqual(report["external_base_salary_reconciliation"]["status"], "pass")
            normalization_args = ["--metrics", str(root/"metrics.json"),
                "--enrollment", str(root/"enrollment.json"),
                "--cpi", str(root/"cpi.json")]
            normalized_path, admin_path = root/"normalized.json", root/"admin.json"
            self.invoke(normalize_metrics.main,
                        normalization_args+["--output", str(normalized_path)])
            self.invoke(admin_overhead.main,
                        normalization_args+["--output", str(admin_path)])
            normalized, admin = self.read_json(normalized_path), self.read_json(admin_path)
            payloads = {"annual-metrics.json": metrics,
                        "normalized-metrics.json": normalized, "admin-overhead.json": admin}
            original_read = Path.read_text
            def read_input(path, *args, **kwargs):
                if path.parent == Path("artifacts/normalized") and path.name in payloads:
                    return json.dumps(payloads[path.name])
                return original_read(path, *args, **kwargs)
            result_path = root/"findings.json"
            with patch.object(Path, "read_text", read_input):
                self.invoke(findings.main, ["--s275-tag", "test-s275",
                    "--normalization-tag", "test-normalization",
                    "--output", str(result_path)])
            self.assertEqual(self.read_json(result_path)["period"]["end"], "2024-25")
            # A failing control must still produce a readable diagnostic report.
            failed = self.read_json(fte_path)
            failed["status"] = "fail"
            failed["years"][0]["status"] = "fail"
            fte_path.write_text(json.dumps(failed))
            with self.assertRaises(SystemExit):
                self.invoke(validation.main, args)
            failed_report = self.read_json(report_path)
            self.assertEqual(failed_report["status"], "fail")
            self.assertIn("external_reconciliation",
                          [item["check"] for item in failed_report["critical"]])

    def test_compensation_parser_reads_real_whitespace_and_page_boundaries(self):
        row = "17407 Riverview 3 0 2.00 100 120 10 20 180"
        text = "Table 38B\n"+row+"\fTable 47\n17407 Riverview 2,819"
        parsed = personnel_compensation.extract_table(text, "Table 38B")
        self.assertEqual(parsed["total_fte"], 2)
        self.assertEqual(parsed["pdf_page"], 1)
        self.assertEqual(parsed["source_row"], row)
