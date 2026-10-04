import unittest
from rsd407_pay.cpi import parse
class CpiTests(unittest.TestCase):
 def test_requires_m13_for_both_series(self):
  data={"status":"REQUEST_SUCCEEDED","Results":{"series":[
   {"seriesID":"CUUR0000SA0","data":[{"year":str(y),"period":"M13","value":str(200+y)} for y in range(2014,2026)]},
   {"seriesID":"CUURS49DSA0","data":[{"year":str(y),"period":"M13","value":str(300+y)} for y in range(2014,2026)]}]}}
  r=parse(data); self.assertEqual(len(r["national_cpi_u"]["values"]),12); self.assertEqual(len(r["seattle_cpi_u"]["values"]),12)
 def test_missing_year_fails(self):
  data={"status":"REQUEST_SUCCEEDED","Results":{"series":[
   {"seriesID":"CUUR0000SA0","data":[{"year":str(y),"period":"M13","value":"1"} for y in range(2014,2026)]},
   {"seriesID":"CUURS49DSA0","data":[{"year":str(y),"period":"M13","value":"1"} for y in range(2014,2025)]}]}}
  with self.assertRaisesRegex(RuntimeError,"missing annual-average years"): parse(data)
if __name__=="__main__": unittest.main()
