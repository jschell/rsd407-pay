import unittest
from io import BytesIO
from openpyxl import Workbook
from rsd407_pay.workbook import validate_workbook_bytes

class WorkbookValidationTests(unittest.TestCase):
    def _xlsx(self, headers):
        wb=Workbook(); ws=wb.active; ws.append(headers); out=BytesIO(); wb.save(out); return out.getvalue()

    def test_accepts_personnel_signature(self):
        data=self._xlsx(["School District","Name","Duty Title","Cert FTE","Clas FTE","Base Salary","Total Salary","Insurance Benefits","Mandatory Benefits"])
        result=validate_workbook_bytes(data,"xlsx")
        self.assertEqual(result["format"],"xlsx")

    def test_rejects_non_personnel_workbook(self):
        data=self._xlsx(["Account","Fund","Program","Amount"])
        with self.assertRaisesRegex(RuntimeError,"S-275 personnel"):
            validate_workbook_bytes(data,"xlsx")

if __name__=="__main__":
    unittest.main()
