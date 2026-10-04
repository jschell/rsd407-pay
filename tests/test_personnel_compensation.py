from rsd407_pay.personnel_compensation import parse_row,extract_table,combine_certificated,consolidated_crosscheck

def test_observed_row_0():
    x=parse_row("17407   Riverview                              217        9,525         210.40       1.52165      76,021     89,961       10,765      20,250    181.0","Table 34B")
    assert x["total_fte"]==210.4
    assert x["average_base_salary_per_fte"]==76021

def test_observed_row_1():
    x=parse_row("17407   Riverview                             215           862         117.06                    51,413      56,180      15,072      12,255    260.0","Table 38B")
    assert x["total_fte"]==117.06
    assert x["average_base_salary_per_fte"]==51413

def test_observed_row_2():
    x=parse_row("17407 Riverview                                      213       9,512         205.02     79,545 94,131        11,941      21,352          183.0","Table 34B")
    assert x["total_fte"]==205.02
    assert x["average_base_salary_per_fte"]==79545

def test_observed_row_3():
    x=parse_row("17407 Riverview                                  16       6,552          15.71 160,784 185,049             11,616     36,083       255.0","Table 36B")
    assert x["total_fte"]==15.71
    assert x["average_base_salary_per_fte"]==160784

def test_observed_row_4():
    x=parse_row("17407 Riverview                                223         1,209        109.81      62,914     68,080      17,871     13,968       260.0","Table 38B")
    assert x["total_fte"]==109.81
    assert x["average_base_salary_per_fte"]==62914

def test_observed_row_5():
    x=parse_row("17407 Riverview                                 215      11,693         212.56 101,877 117,437             13,200     19,737       188.7","Table 37C")
    assert x["total_fte"]==212.56
    assert x["average_base_salary_per_fte"]==101877

def test_observed_row_6():
    x=parse_row("17407 Riverview                                   219       12,406         211.45    107,865     124,367      16,525      20,163      185.8","Table 37C")
    assert x["total_fte"]==211.45
    assert x["average_base_salary_per_fte"]==107865

def test_observed_row_7():
    x=parse_row("17407 Riverview                                   250          246         125.91      75,138 100,708         29,402      16,651      260.0","Table 38B")
    assert x["total_fte"]==125.91
    assert x["average_base_salary_per_fte"]==75138

def test_repeated_headings_are_page_scoped():
    text="Table 38B: Classified Staff in All Programs\\fTable 38B: Classified Staff in All Programs\\n17407 Riverview 250 246 125.91 75,138 100,708 29,402 16,651 260.0\\fTable 38B: Classified Staff in All Programs"
    x=extract_table(text,"Table 38B")
    assert x["pdf_page"]==2 and x["total_fte"]==125.91

def test_consolidated_crosscheck():
    a=parse_row("17407 Riverview 199 11,790 196.70 95,554 110,796 13,200 18,740 183.0","Table 34B"); a.update({"table":"Table 34B","pdf_page":281})
    b=parse_row("17407 Riverview 16 6,186 15.86 180,300 199,800 13,200 32,102 259.9","Table 36B"); b.update({"table":"Table 36B","pdf_page":320})
    c=parse_row("17407 Riverview 215 11,693 212.56 101,877 117,437 13,200 19,737 188.7","Table 37C")
    check=consolidated_crosscheck(c,[a,b])
    assert abs(check["fte_difference"])<1e-9
    assert abs(check["implied_total_differences"]["average_base_salary_per_fte"])<100


def test_extract_table_uses_real_form_feed_pages():
    text="Table 38B: Classified Staff in All Programs\nheader only\fTable 38B: Classified Staff in All Programs\n17407 Riverview 250 246 125.91 75,138 100,708 29,402 16,651 260.0\n"
    row=extract_table(text,"Table 38B")
    assert row["pdf_page"]==2
    assert row["total_fte"]==125.91
