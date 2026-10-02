import unittest
from rsd407_pay.metrics import aggregate

class MetricsTests(unittest.TestCase):
    def test_aggregate_and_reconciliation(self):
        rows=[
            {"school_year":"2024-25","job_family":"teachers","certificated_fte":"1","classified_fte":"0","base_salary":"100","total_salary":"120","insurance_benefits":"10","mandatory_benefits":"20"},
            {"school_year":"2024-25","job_family":"other classified","certificated_fte":"0","classified_fte":".5","base_salary":"40","total_salary":"35","insurance_benefits":"5","mandatory_benefits":"6"},
            {"school_year":"2024-25","job_family":"other classified","certificated_fte":"0","classified_fte":"0","base_salary":"2","total_salary":"2","insurance_benefits":"0","mandatory_benefits":"0"},
        ]
        r=aggregate(rows); d=r["district"][0]
        self.assertEqual(d["employee_rows"],3)
        self.assertAlmostEqual(d["total_fte"],1.5)
        self.assertEqual(d["zero_fte_rows"],1)
        self.assertEqual(d["total_salary_below_base_rows"],1)
        self.assertAlmostEqual(sum(x["total_fte"] for x in r["categories"]),d["total_fte"])
        self.assertAlmostEqual(sum(x["base_salary"] for x in r["categories"]),d["base_salary"])
        self.assertAlmostEqual(sum(x["total_salary"] for x in r["categories"]),d["total_salary"])
        self.assertAlmostEqual(sum(x["insurance_benefits"] for x in r["categories"]),d["insurance_benefits"])
        self.assertAlmostEqual(sum(x["mandatory_benefits"] for x in r["categories"]),d["mandatory_benefits"])
        self.assertAlmostEqual(d["reported_employer_compensation"],198)
        self.assertAlmostEqual(d["reported_employer_compensation"], d["total_salary"] + d["insurance_benefits"] + d["mandatory_benefits"])
if __name__=="__main__": unittest.main()
