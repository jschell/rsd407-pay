import unittest
from rsd407_pay.normalize_metrics import build,YEARS

class NormalizeMetricsTests(unittest.TestCase):
    def fixtures(self):
        district=[]
        enrollment=[]
        for sy in YEARS:
            district.append({"school_year":sy,"employee_rows":100,"total_fte":50,
                "base_salary":1000,"total_salary":1200,"reported_employer_compensation":1500})
            enrollment.append({"school_year":sy,"student_fte":1000,
                "measure":"P-223 final annual-average K-12 FTE including ALE"})
        values={str(y):100+(y-2014)*10 for y in range(2014,2026)}
        cpi={"series":{n:{"series_id":n,"geography":n,"values":dict(values)}
             for n in ("national_cpi_u","seattle_cpi_u")}}
        return {"district":district},{"years":enrollment},cpi
    def test_per_student_and_per_1000(self):
        m,e,c=self.fixtures(); r=build(m,e,c)["years"][0]
        self.assertEqual(r["employee_rows_per_1000_student_fte"],100)
        self.assertEqual(r["staff_fte_per_1000_student_fte"],50)
        self.assertEqual(r["total_salary_per_student_fte"],1.2)
    def test_constant_dollar_formula(self):
        m,e,c=self.fixtures(); r=build(m,e,c)["years"][0]
        factor=c["series"]["national_cpi_u"]["values"]["2025"]/c["series"]["national_cpi_u"]["values"]["2014"]
        self.assertAlmostEqual(r["constant_2025_dollars"]["national_cpi_u"]["total_salary"],1200*factor)
    def test_missing_enrollment_fails(self):
        m,e,c=self.fixtures(); e["years"].pop()
        with self.assertRaisesRegex(RuntimeError,"exact 2013-14"): build(m,e,c)
if __name__=="__main__": unittest.main()
