from rsd407_pay.personnel_compensation_compare import compare
def test_combines_certificated_and_classified_controls_without_allocating_rows():
    controls={"district_code":"17407","years":[{"school_year":"2024-25","source_sha256":"abc","controls":{
      "certificated":{"total_fte":2,"average_base_salary_per_fte":100,"average_total_salary_per_fte":120,"average_insurance_benefits_per_fte":10,"average_mandatory_benefits_per_fte":20},
      "classified":{"total_fte":1,"average_base_salary_per_fte":50,"average_total_salary_per_fte":60,"average_insurance_benefits_per_fte":5,"average_mandatory_benefits_per_fte":10}}}]}
    metrics={"district":[{"school_year":"2024-25","base_salary":250,"total_salary":300,"insurance_benefits":25,"mandatory_benefits":50}]}
    r=compare(controls,metrics)["years"][0]["combined_all_programs"]
    assert r["base_salary"]["ospi_implied_total"]==250
    assert r["total_salary"]["difference"]==0
