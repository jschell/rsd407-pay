import unittest
from rsd407_pay.personnel_compensation_compare import compare,product_rounding_bound

class CompensationComparisonTests(unittest.TestCase):
    def test_rounding_bound_uses_published_precision(self):
        assert product_rounding_bound(100.0,100000)>0
    def test_base_salary_is_gate_other_fields_are_semantic_review(self):
        controls={"district_code":"17407","years":[{"school_year":"2024-25","source_sha256":"abc","compensation_rows":[
          {"table":"Table 37C","total_fte":2,"average_base_salary_per_fte":100,"average_total_salary_per_fte":120,"average_insurance_benefits_per_fte":10,"average_mandatory_benefits_per_fte":20},
          {"table":"Table 38B","total_fte":1,"average_base_salary_per_fte":50,"average_total_salary_per_fte":60,"average_insurance_benefits_per_fte":5,"average_mandatory_benefits_per_fte":10}]}]}
        metrics={"district":[{"school_year":"2024-25","base_salary":250,"total_salary":300,"insurance_benefits":25,"mandatory_benefits":50}]}
        r=compare(controls,metrics)
        assert r["status"]=="pass"
        assert r["years"][0]["combined_all_programs"]["base_salary"]["status"]=="pass"
        assert r["years"][0]["combined_all_programs"]["total_salary"]["status"]=="semantic_review"
    