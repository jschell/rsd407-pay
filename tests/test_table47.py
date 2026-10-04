import unittest
from rsd407_pay.table47 import build_control_inventory
class Table47Tests(unittest.TestCase):
    def test_annual_pdf_becomes_embedded_table47_source(self):
        inv={"resources":[
            {"school_year":"2024-25","label":"2024-25 Personnel Summary Report","url":"u","extension":".pdf"},
            {"school_year":"2024-25","label":"2024-25 Personnel Summary workbook","url":"x","extension":".xlsx"}]}
        r=build_control_inventory(inv)
        self.assertEqual(r["covered_years"],["2024-25"])
        self.assertEqual(len(r["resources"]),1)
        self.assertEqual(r["resources"][0]["table"],"47")
        self.assertEqual(r["resources"][0]["source_mode"],"embedded")
        self.assertEqual(r["fields"]["student_fte"]["status"],"comparable")
        self.assertEqual(r["fields"]["average_salary"]["status"],"candidate")
if __name__=="__main__": unittest.main()
