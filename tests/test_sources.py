import unittest
from unittest.mock import patch
from rsd407_pay.sources import Links, discover, normalize_year, s275_section

class SourceTests(unittest.TestCase):
    def test_year_variants(self):
        self.assertEqual(normalize_year("School Year 2013-14 Excel"),"2013-14")
        self.assertEqual(normalize_year("2024–2025 personnel"),"2024-25")

    def test_links(self):
        p=Links();p.feed('<a href="/a.xlsx">2019-20 Excel</a>')
        self.assertEqual(p.links,[("/a.xlsx","2019-20 Excel")])

    def test_heading_detected_through_markup(self):
        html='<h2>Personnel <strong>Reporting Data</strong> (S-275)</h2>'
        self.assertEqual(s275_section(html),html)

    def test_discovery_rejects_f196_same_year(self):
        html=b'''<html><body><a href="/wrong.xlsx">2024-25 F-196 Codes</a>
        <h2>Personnel <strong>Reporting Data</strong> (S-275)</h2>
        <a href="/right.xlsx">Washington State School Personnel - School Year 2024-25</a></body></html>'''
        cfg={"landing_page":"https://ospi.k12.wa.us/safs-data-files","allowed_hosts":["ospi.k12.wa.us"],"preferred_formats":["xlsx"],"expected_final_years":["2024-25"]}
        meta={"status":200,"content_type":"text/html","final_url":cfg["landing_page"]}
        with patch("rsd407_pay.sources.fetch",return_value=(html,meta)):
            rows=discover(cfg)
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0].direct_download_url.endswith("/right.xlsx"))
