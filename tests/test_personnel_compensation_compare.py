from rsd407_pay.personnel_compensation_compare import compare,product_rounding_bound

def test_rounding_bound_is_derived_from_published_precision():
    assert product_rounding_bound(100.00,100000) > 0

def test_combines_controls_and_assesses_rounding():
    controls={"district_code":"17407","years":[{"school_year":"2024-25","source_sha256":"abc","controls":{
      "certificated_control_tables":["Table 37C"],
      "certificated":{"source_table":"Table 37C","total_fte":2,"average_base_salary_per_fte":100,"average_total_salary_per_fte":120,"average_insurance_benefits_per_fte":10,"average_mandatory_benefits_per_fte":20},
      "classified":{"source_table":"Table 38B","total_fte":1,"average_base_salary_per_fte":50,"average_total_salary_per_fte":60,"average_insurance_benefits_per_fte":5,"average_mandatory_benefits_per_fte":10}}}]}
    metrics={"district":[{"school_year":"2024-25","base_salary":250,"total_salary":300,"insurance_benefits":25,"mandatory_benefits":50}]}
    r=compare(controls,metrics)
    assert r["status"]=="pass_display_rounding_only"
    assert r["years"][0]["combined_all_programs"]["base_salary"]["difference"]==0
