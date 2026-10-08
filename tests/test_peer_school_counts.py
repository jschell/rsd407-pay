import unittest
from rsd407_pay.peer_school_counts import enrich

class SchoolCountTests(unittest.TestCase):
 def test_school_and_central_roles_separate(self):
  report={'rows':[{'school_year':'2024-25','district':'Riverview','district_code':'17407','school_admin_fte':12,'central_fte':4}]}
  schools=[{'districtcode':'17407','schoolcode':str(i)} for i in range(8)]
  result=enrich(report,schools)[0]
  self.assertEqual(result['school_admin_fte_per_reporting_school'],1.5)
  self.assertEqual(result['central_admin_fte_per_reporting_school'],.5)
  with self.assertRaisesRegex(RuntimeError,'duplicate'):enrich(report,schools+[schools[0]])
  with self.assertRaisesRegex(RuntimeError,'missing'):enrich(report,[])
