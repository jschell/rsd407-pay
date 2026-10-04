import unittest
from io import BytesIO
from openpyxl import Workbook
from rsd407_pay.enrollment_inventory import inventory
class EnrollmentInventoryTests(unittest.TestCase):
 def test_inventory_preserves_sheet_and_rows(self):
  wb=Workbook(); ws=wb.active; ws.title="Enrollment"; ws.append(["District","Year","AAFTE"]); ws.append(["Riverview","2024-25",3000])
  b=BytesIO(); wb.save(b); r=inventory(b.getvalue())
  self.assertEqual(r["sheets"][0]["title"],"Enrollment")
  self.assertEqual(r["sheets"][0]["first_nonempty_rows"][0],["District","Year","AAFTE"])
if __name__=="__main__": unittest.main()
