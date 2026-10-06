import unittest
from decimal import Decimal
from rsd407_pay.table45b_reconcile import (
    COMPONENT_ROUNDING_TOLERANCE, parse_table45b_text, reconcile,
)

class Table45BTests(unittest.TestCase):
    def test_parser_ignores_rank_and_stops_before_later_tables(self):
        text = """Table 45B: All Programs
  90  17407 Riverview  2,819  196.19  14.37  69.60  15.26  184.72  5.41  125.91  22.39  44.67
Table 46: Another Table
  88  17407 Riverview  999.99  888.88  777.77
"""
        self.assertEqual(parse_table45b_text(text)["total_fte"], 337.36)

    def test_component_rounding_bound(self):
        self.assertLessEqual(abs(Decimal("337.367")-Decimal("337.36")),
                             COMPONENT_ROUNDING_TOLERANCE)

    def test_committed_control_schema_passes(self):
        controls = {"years": [{"school_year": "2024-25", "source_sha256": "abc",
                               "table45b": {"total_fte": 337.36}}]}
        metrics = {"district": [{"school_year": "2024-25", "total_fte": 337.367}]}
        report = reconcile(controls, metrics)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["years"][0]["project_total_fte"], 337.367)
        metrics["district"][0]["total_fte"] = 337.40
        self.assertEqual(reconcile(controls, metrics)["status"], "fail")
