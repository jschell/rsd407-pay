import unittest
from rsd407_pay.source_warning_review import summarize

class SourceWarningTests(unittest.TestCase):
    def test_counts_overlap_without_double_counting_salary(self):
        rows = [dict(certificated_fte=0, classified_fte=0, base_salary=100, total_salary=20),
                dict(certificated_fte=1, classified_fte=0, base_salary=100, total_salary=50),
                dict(certificated_fte=1, classified_fte=0, base_salary=100, total_salary=120)]
        self.assertEqual(summarize(rows), {'zero_fte_rows': 1, 'zero_fte_total_salary': 20,
            'salary_below_base_rows': 2, 'salary_below_base_gap': 130})
