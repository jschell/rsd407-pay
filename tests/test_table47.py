import unittest
from rsd407_pay.table47 import build_control_inventory
class Table47Tests(unittest.TestCase):
    def test_selects_table47_only(self):
        inv={"resources":[{"school_year":"2024-25","label":"Table 47 Selected Personnel Data by School District","url":"u","extension":".pdf"},{"school_year":"2024-25","label":"Table 45","url":"x","extension":".pdf"}]}
        r=build_control_inventory(inv)
        self.assertEqual(r["covered_years"],["2024-25"])
        self.assertEqual(len(r["resources"]),1)
        self.assertEqual(r["fields"]["student_fte"]["status"],"comparable")
        self.assertEqual(r["fields"]["average_salary"]["status"],"candidate")
if __name__=="__main__": unittest.main()
