import unittest
from rsd407_pay.sources import Links, normalize_year, s275_section
class SourceTests(unittest.TestCase):
    def test_year_variants(self):
        self.assertEqual(normalize_year("School Year 2013-14 Excel"),"2013-14")
        self.assertEqual(normalize_year("2024–2025 personnel"),"2024-25")
    def test_links(self):
        p=Links();p.feed('<a href="/a.xlsx">2019-20 Excel</a>');self.assertEqual(p.links,[("/a.xlsx","2019-20 Excel")])
    def test_section_excludes_f196(self):
        html='F-196 <a href="/wrong.xlsx">2024-25 F-196 Codes</a> Personnel Reporting Data (S-275) <a href="/right.xlsx">Washington State School Personnel - School Year 2024-25</a> Apportionment Data Files'
        section=s275_section(html)
        self.assertIn("right.xlsx",section);self.assertNotIn("wrong.xlsx",section)
