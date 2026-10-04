from decimal import Decimal
from rsd407_pay.table45b_reconcile import parse_table45b_text, q2

def test_parse_table45b_riverview_row():
    text="""Table 45B: Comparison of Certificated and Classified FTE Staff in All Programs with FTE Students\n  90  17407 Riverview  196.19  15.26  125.91  2,819  14.37  22.39\nTable 46"""
    row=parse_table45b_text(text)
    assert row["total_fte"] == 337.36

def test_comparison_uses_published_precision():
    assert q2(Decimal("337.367")) == q2(Decimal("337.36"))


def test_reconcile_uses_district_metrics_schema(monkeypatch, tmp_path):
    from rsd407_pay import table45b_reconcile as m
    pdf=tmp_path/"x.pdf"; pdf.write_bytes(b"%PDF")
    monkeypatch.setattr(m,"extract",lambda p: {"certificated_instructional_fte":196.19,"certificated_administrative_fte":15.26,"classified_fte":125.91,"total_fte":337.36})
    manifest={"resources":[{"school_year":"2024-25","local_file":str(pdf),"sha256":"abc"}]}
    metrics={"district":[{"school_year":"2024-25","total_fte":337.367}]}
    report=m.reconcile(manifest,metrics)
    assert report["status"]=="pass"
    assert report["years"][0]["project_total_fte"]==337.367
