import json, tempfile, unittest
from pathlib import Path
from rsd407_pay.duty_coverage import build_coverage

class DutyVocabularyTests(unittest.TestCase):
    def test_titles_are_exact_sorted_source_values(self):
        report=build_coverage([
            {"school_year":"2024-25","duty_title":"Technical","certificated_fte":"0","classified_fte":"1"},
            {"school_year":"2024-25","duty_title":"Aide","certificated_fte":"0","classified_fte":".5"},
        ])
        self.assertEqual(list(report["titles"]),["Aide","Technical"])
        self.assertEqual(report["titles"]["Aide"]["classified_fte"],.5)
if __name__=="__main__": unittest.main()
