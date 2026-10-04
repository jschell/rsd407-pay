import unittest
from rsd407_pay.enrollment_source import discover
class EnrollmentSourceTests(unittest.TestCase):
 def test_discovers_exact_final_summary(self):
  h='<a href="/sites/default/files/final.xlsx">Final Enrollment Summary - For the School Years 2001-02 through 2024-2025</a>'
  s=discover(h); self.assertEqual(s.workbook_url,"https://ospi.k12.wa.us/sites/default/files/final.xlsx")
 def test_title_change_fails(self):
  with self.assertRaisesRegex(RuntimeError,"not found"): discover('<a href="/wrong.xlsx">Enrollment Summary</a>')
 def test_external_host_fails(self):
  h='<a href="https://example.com/final.xlsx">Final Enrollment Summary - For the School Years 2001-02 through 2024-2025</a>'
  with self.assertRaisesRegex(RuntimeError,"unexpected"): discover(h)
if __name__=="__main__": unittest.main()
