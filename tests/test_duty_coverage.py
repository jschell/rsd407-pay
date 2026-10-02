import unittest
from rsd407_pay.duty_coverage import build_coverage

class DutyCoverageTests(unittest.TestCase):
    def test_preserves_exact_titles_and_cert_class_fte(self):
        rows = [
            {"school_year":"2024-25","duty_title":"Teacher","certificated_fte":"1","classified_fte":"0"},
            {"school_year":"2024-25","duty_title":"Aide","certificated_fte":"0","classified_fte":"0.5"},
            {"school_year":"2023-24","duty_title":"Teacher","certificated_fte":"0.8","classified_fte":"0"},
        ]
        r=build_coverage(rows)
        self.assertEqual(set(r["titles"]), {"Teacher","Aide"})
        self.assertEqual(r["titles"]["Teacher"]["rows"], 2)
        self.assertAlmostEqual(r["titles"]["Teacher"]["certificated_fte"], 1.8)
        self.assertEqual(r["titles"]["Aide"]["classified_fte"], 0.5)
        self.assertEqual(r["titles"]["Teacher"]["years"], ["2023-24","2024-25"])

    def test_missing_title_is_explicit(self):
        r=build_coverage([{"school_year":"2024-25","duty_title":"","certificated_fte":"0","classified_fte":"0"}])
        self.assertIn("__MISSING__", r["titles"])

if __name__=="__main__":
    unittest.main()
