import unittest
from rsd407_pay.sources import Links, normalize_year

class SourceTests(unittest.TestCase):
    def test_year_variants(self):
        self.assertEqual(normalize_year("School Year 2013-14 Excel"),"2013-14")
        self.assertEqual(normalize_year("2024–2025 personnel"),"2024-25")
        self.assertIsNone(normalize_year("S-275 data"))
    def test_links(self):
        p=Links(); p.feed('<a href="/a.xlsx">2019-20 Excel</a>')
        self.assertEqual(p.links,[("/a.xlsx","2019-20 Excel")])

if __name__=="__main__": unittest.main()
