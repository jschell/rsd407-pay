import unittest
from rsd407_pay.quality import build_quality_report

class QualityTests(unittest.TestCase):
    def test_reports_conditions_without_repairing(self):
        rows=[
          {"school_year":"2024-25","job_family":"teachers","certificated_fte":"1","classified_fte":"0","base_salary":"100","total_salary":"120"},
          {"school_year":"2024-25","job_family":"other classified","certificated_fte":"0","classified_fte":"0","base_salary":"50","total_salary":"40"},
        ]
        r=build_quality_report(rows)
        self.assertEqual(r["annual"][0]["zero_fte_rows"],1)
        self.assertEqual(r["annual"][0]["total_salary_below_base_rows"],1)
        self.assertEqual(len(r["by_job_family"]),1)
        self.assertEqual(r["by_job_family"][0]["job_family"],"other classified")
        self.assertIn("not evidence of payroll error",r["interpretation"]["warning"])
if __name__=="__main__": unittest.main()
