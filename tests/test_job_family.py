import unittest
from rsd407_pay.job_family import apply,coverage

class JobFamilyTests(unittest.TestCase):
    def test_exact_mapping_and_unknown(self):
        cfg={"mappings":{"Aide":"paraeducators/instructional aides"}}
        rows=[{"school_year":"2024-25","duty_title":"Aide","certificated_fte":"0","classified_fte":"0.5"},{"school_year":"2024-25","duty_title":"New Title","certificated_fte":"0","classified_fte":"1"}]
        out,unknown=apply(rows,cfg)
        self.assertEqual(out[0]["job_family"],"paraeducators/instructional aides")
        self.assertEqual(out[1]["job_family"],"unmapped/review")
        self.assertEqual(unknown,["New Title"])
    def test_coverage(self):
        rows=[{"school_year":"2024-25","job_family":"teachers","certificated_fte":"1","classified_fte":"0"}]
        self.assertEqual(coverage(rows)[0]["total_fte"],1.0)
if __name__=="__main__": unittest.main()
