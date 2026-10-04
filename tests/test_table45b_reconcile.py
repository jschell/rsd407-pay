from decimal import Decimal
from rsd407_pay.table45b_reconcile import COMPONENT_ROUNDING_TOLERANCE, parse_table45b_text

def test_parse_table45b_riverview_row():
    text="""Table 45B: Comparison of Certificated and Classified FTE Staff in All Programs with FTE Students\n  90  17407 Riverview  2,819  196.19  14.37  69.60  15.26  184.72  5.41  125.91  22.39  44.67\nTable 46"""
    row=parse_table45b_text(text)
    assert row["total_fte"] == 337.36

def test_comparison_uses_component_rounding_bound():
    assert abs(Decimal("337.367")-Decimal("337.36")) <= COMPONENT_ROUNDING_TOLERANCE


def test_reconcile_uses_district_metrics_schema(monkeypatch, tmp_path):
    from rsd407_pay import table45b_reconcile as m
    pdf=tmp_path/"x.pdf"; pdf.write_bytes(b"%PDF")
    monkeypatch.setattr(m,"extract",lambda p: {"certificated_instructional_fte":196.19,"certificated_administrative_fte":15.26,"classified_fte":125.91,"total_fte":337.36})
    manifest={"resources":[{"school_year":"2024-25","local_file":str(pdf),"sha256":"abc"}]}
    metrics={"district":[{"school_year":"2024-25","total_fte":337.367}]}
    report=m.reconcile(manifest,metrics)
    assert report["status"]=="pass"
    assert report["years"][0]["project_total_fte"]==337.367


def test_parser_stops_before_later_tables():
    text="""Table 45B: Comparison of Certificated and Classified FTE Staff in All Programs with FTE Students\n  90  17407 Riverview  2,819  196.19  14.37  69.60  15.26  184.72  5.41  125.91  22.39  44.67\nTable 46: Another District Table\n  88  17407 Riverview  999.99  888.88  777.77\nTable 47: School Districts Ranked by FTE Enrollment (Report P-223)\n  90  17407 Riverview  2,819\n"""
    row=parse_table45b_text(text)
    assert row["total_fte"] == 337.36


def test_component_rounding_bound_rejects_material_difference(monkeypatch, tmp_path):
    from rsd407_pay import table45b_reconcile as m
    pdf=tmp_path/"x.pdf"; pdf.write_bytes(b"%PDF")
    monkeypatch.setattr(m,"extract",lambda p: {"certificated_instructional_fte":196.19,"certificated_administrative_fte":15.26,"classified_fte":125.91,"total_fte":337.36})
    report=m.reconcile({"resources":[{"school_year":"2024-25","local_file":str(pdf),"sha256":"abc"}]},{"district":[{"school_year":"2024-25","total_fte":337.40}]})
    assert report["status"]=="fail"
