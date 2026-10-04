from decimal import Decimal
from rsd407_pay.table45b_reconcile import parse_table45b_text, q2

def test_parse_table45b_riverview_row():
    text="""Table 45B: Comparison of Certificated and Classified FTE Staff in All Programs with FTE Students\n  90  17407 Riverview  196.19  15.26  125.91  2,819  14.37  22.39\nTable 46"""
    row=parse_table45b_text(text)
    assert row["total_fte"] == 337.36

def test_comparison_uses_published_precision():
    assert q2(Decimal("337.367")) == q2(Decimal("337.36"))
