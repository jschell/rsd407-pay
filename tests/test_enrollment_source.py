import unittest
from rsd407_pay.enrollment_source import discover

class EnrollmentSourceTests(unittest.TestCase):
    def test_discovers_exact_final_summary(self):
        h='<a href="/sites/default/files/final.xlsx">Final Enrollment Summary - For the School Years 2001-02 through 2024-2025</a>'
        s=discover(h)
        self.assertEqual(s.workbook_url,"https://ospi.k12.wa.us/sites/default/files/final.xlsx")

    def test_discovers_title_through_nested_markup(self):
        h='<a class="file" href="/final.xlsx"><span>Final Enrollment Summary</span> - For the School Years 2001-02 through 2024-2025</a>'
        self.assertEqual(discover(h).workbook_url,"https://ospi.k12.wa.us/final.xlsx")

    def test_title_change_fails(self):
        with self.assertRaisesRegex(RuntimeError,"expected once"):
            discover('<a href="/wrong.xlsx">Enrollment Summary</a>')

    def test_duplicate_exact_title_fails(self):
        h='<a href="/one.xlsx">'+__import__("rsd407_pay.enrollment_source",fromlist=["LINK_TEXT"]).LINK_TEXT+'</a><a href="/two.xlsx">'+__import__("rsd407_pay.enrollment_source",fromlist=["LINK_TEXT"]).LINK_TEXT+'</a>'
        with self.assertRaisesRegex(RuntimeError,"found 2"):
            discover(h)

    def test_external_host_fails(self):
        h='<a href="https://example.com/final.xlsx">Final Enrollment Summary - For the School Years 2001-02 through 2024-2025</a>'
        with self.assertRaisesRegex(RuntimeError,"unexpected"):
            discover(h)

if __name__=="__main__": unittest.main()
