from rsd407_pay.personnel_compensation import parse_control
def test_parse_table37c_compensation_row():
    text="""Table 37C: Certificated Staff in All Programs
17407 Riverview                                   219       12,406         211.45    107,865     124,367      16,525      20,163      185.8
Table 38: Classified Staff in Basic Education Programs
"""
    row=parse_control(text,"Table 37C")
    assert row["individuals"]==219 and row["total_fte"]==211.45
    assert row["average_base_salary_per_fte"]==107865.0 and row["average_total_salary_per_fte"]==124367.0
def test_parse_table38b_compensation_row():
    text="""Table 38B: Classified Staff in All Programs
17407 Riverview                                   250          246         125.91      75,138 100,708         29,402      16,651      260.0
Table 39: Other
"""
    row=parse_control(text,"Table 38B")
    assert row["individuals"]==250 and row["total_fte"]==125.91
    assert row["average_insurance_benefits_per_fte"]==29402.0


def test_combine_legacy_certificated_tables():
    from rsd407_pay.personnel_compensation import combine_certificated
    parts=[{"total_fte":2.0,"average_base_salary_per_fte":100.0,"average_total_salary_per_fte":120.0,"average_insurance_benefits_per_fte":10.0,"average_mandatory_benefits_per_fte":20.0},
           {"total_fte":1.0,"average_base_salary_per_fte":200.0,"average_total_salary_per_fte":240.0,"average_insurance_benefits_per_fte":20.0,"average_mandatory_benefits_per_fte":40.0}]
    row=combine_certificated(parts)
    assert row["total_fte"]==3.0
    assert abs(row["average_base_salary_per_fte"]-(400/3))<1e-9
