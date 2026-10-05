from rsd407_pay.verify_s275_access_controls import verify
def row(year="2024-25"):
    return {"school_year":year,"personnel_rows":442,"total_fte":337.367,"base_salary":32268498.0,"total_salary":36149348.0,"insurance":6962808.0,"mandatory_benefits":5876180.0,"reported_employer_compensation":48988336.0,"source_sha256":"a","database_sha256":"b","table":"T"}
def test_equal_controls_pass():
    d={"district_code":"17407","years":[row()]};a={"district_code":"17407","years":[row()]}
    assert verify(d,a)==[]
def test_drift_is_visible():
    d={"district_code":"17407","years":[row()]};r=row();r["base_salary"]+=1;a={"district_code":"17407","years":[r]}
    assert any("base_salary drift" in x for x in verify(d,a))
