import unittest
from rsd407_pay.metrics import aggregate,validate_reconciliation

class MetricsTests(unittest.TestCase):
    def rows(self):
        return [
            {"school_year":"2023-24","job_family":"teachers","certificated_fte":"1","classified_fte":"0","base_salary":"80","total_salary":"100","insurance_benefits":"8","mandatory_benefits":"12"},
            {"school_year":"2024-25","job_family":"teachers","certificated_fte":"1","classified_fte":"0","base_salary":"100","total_salary":"120","insurance_benefits":"10","mandatory_benefits":"20"},
            {"school_year":"2024-25","job_family":"other classified","certificated_fte":"0","classified_fte":".5","base_salary":"40","total_salary":"35","insurance_benefits":"5","mandatory_benefits":"6"},
            {"school_year":"2024-25","job_family":"other classified","certificated_fte":"0","classified_fte":"0","base_salary":"2","total_salary":"2","insurance_benefits":"0","mandatory_benefits":"0"},
        ]

    def test_aggregate_reconciliation_quality_and_changes(self):
        r=aggregate(self.rows()); d=r["district"][1]
        self.assertEqual(r["baseline_school_year"],"2023-24")
        self.assertEqual(d["employee_rows"],3); self.assertAlmostEqual(d["total_fte"],1.5)
        self.assertEqual(d["zero_fte_rows"],1); self.assertEqual(d["total_salary_below_base_rows"],1)
        self.assertAlmostEqual(d["reported_employer_compensation"],198)
        self.assertAlmostEqual(d["reported_employer_compensation"],d["total_salary"]+d["insurance_benefits"]+d["mandatory_benefits"])
        self.assertAlmostEqual(d["change"]["total_salary"]["year_over_year"]["absolute"],57)
        self.assertAlmostEqual(d["change"]["total_salary"]["year_over_year"]["percent"],.57)
        self.assertAlmostEqual(d["change"]["total_salary"]["from_baseline"]["percent"],.57)

    def test_runtime_reconciliation_rejects_mismatch(self):
        district=[{"school_year":"2024-25","employee_rows":1,"certificated_fte":1,"classified_fte":0,"base_salary":100,"total_salary":100,"insurance_benefits":0,"mandatory_benefits":0,"total_fte":1,"reported_employer_compensation":100,"zero_fte_rows":0,"total_salary_below_base_rows":0}]
        category=[dict(district[0],base_salary=99,job_family="teachers")]
        with self.assertRaises(RuntimeError): validate_reconciliation(district,category)

if __name__=="__main__": unittest.main()
