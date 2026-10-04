import unittest
from rsd407_pay.personnel_summary import inventory
class PersonnelSummaryTests(unittest.TestCase):
    def test_inventory(self):
        html='<a href="/x.pdf">2013-14 Personnel Summary Report</a><a href="/45.xlsx">2013-14 Table 45 and 45B</a>'
        r=inventory(html,"https://example.test/page")
        self.assertEqual(r["covered_years"],["2013-14"])
        self.assertEqual(len(r["resources"]),2)
        self.assertEqual(r["resources"][0]["url"],"https://example.test/x.pdf")
if __name__=="__main__": unittest.main()
