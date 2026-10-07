import unittest
from rsd407_pay.reporting import category_changes, require_gate, table

class ReportingTests(unittest.TestCase):
    def test_staffing_intensity_uses_each_years_enrollment(self):
        metrics={'categories':[{'school_year':'2013-14','job_family':'teachers','employee_rows':10,'total_fte':8,'total_salary':80},
                               {'school_year':'2024-25','job_family':'teachers','employee_rows':10,'total_fte':8,'total_salary':100}]}
        norm={'years':[{'school_year':'2013-14','student_fte':1000}, {'school_year':'2024-25','student_fte':800}]}
        row=category_changes(metrics,norm)[0]
        self.assertEqual(row['fte_change'],0)
        self.assertEqual(row['intensity_change'],2)
        self.assertEqual(row['nominal_total_salary_change'],20)
        metrics['categories'].pop()
        with self.assertRaises(RuntimeError):
            category_changes(metrics,norm)

    def test_failed_or_missing_validation_blocks_publication(self):
        for status in ('fail','pending',None):
            with self.assertRaises(RuntimeError):
                require_gate({'status':status},'test')
        require_gate({'status':'pass'},'test')

    def test_markdown_labels_cannot_break_table_columns(self):
        rendered=table(['category','value'],[['a|b',10]])
        self.assertEqual(rendered[-1],'| a/b | 10 |')
