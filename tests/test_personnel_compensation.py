from rsd407_pay.personnel_compensation import parse_control,combine_certificated

def test_2019_certificated_staff_mix_schema():
    text="""Table 34B: Certificated Instructional Staff in All Programs
17407 Riverview 217 9,525 210.40 1.52165 76,021 89,961 10,765 20,250 181.0
Table 35: next
"""
    row=parse_control(text,"Table 34B")
    assert row["total_fte"]==210.40
    assert row["staff_mix_defunct"]==1.52165
    assert row["average_base_salary_per_fte"]==76021

def test_normal_compensation_schema():
    text="""Table 38B: Classified Staff in All Programs
17407 Riverview 250 246 125.91 75,138 100,708 29,402 16,651 260.0
Table 39: next
"""
    row=parse_control(text,"Table 38B")
    assert row["individuals"]==250 and row["total_fte"]==125.91
    assert row["average_insurance_benefits_per_fte"]==29402

def test_repeated_headings_resolve_one_unique_row():
    text="""Table 38B: Classified Staff in All Programs
header only
Table 38B: Classified Staff in All Programs
17407 Riverview 250 246 125.91 75,138 100,708 29,402 16,651 260.0
Table 39: next
"""
    assert parse_control(text,"Table 38B")["total_fte"]==125.91

def test_unknown_numeric_schema_fails():
    text="""Table 38B: Classified Staff in All Programs
17407 Riverview 1 2 3 4 5 6
Table 39: next
"""
    import pytest
    with pytest.raises(RuntimeError,match="unsupported"):
        parse_control(text,"Table 38B")

def test_combine_legacy_certificated_tables():
    parts=[{"source_table":"Table 34B","total_fte":2.0,"average_base_salary_per_fte":100.0,"average_total_salary_per_fte":120.0,"average_insurance_benefits_per_fte":10.0,"average_mandatory_benefits_per_fte":20.0},
           {"source_table":"Table 36B","total_fte":1.0,"average_base_salary_per_fte":200.0,"average_total_salary_per_fte":240.0,"average_insurance_benefits_per_fte":20.0,"average_mandatory_benefits_per_fte":40.0}]
    row=combine_certificated(parts)
    assert row["total_fte"]==3.0
    assert abs(row["average_base_salary_per_fte"]-(400/3))<1e-9
