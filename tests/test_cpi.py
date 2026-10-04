import unittest
from unittest.mock import patch
import rsd407_pay.cpi as cpi
from rsd407_pay.cpi import parse

def rows(series_id,count):
    return {"seriesID":series_id,"data":[{"year":str(y),"period":f"M{m:02d}","value":str(y+m/100)} for y in range(2014,2026) for m in range(1,count+1)]}

class CpiTests(unittest.TestCase):
    def test_fetch_merges_bounded_windows(self):
        def window(start,end):
            return {"status":"REQUEST_SUCCEEDED","Results":{"series":[
                {"seriesID":"CUUR0000SA0","data":[{"year":str(y),"period":"M01","value":"1"} for y in range(start,end+1)]},
                {"seriesID":"CUURS49DSA0","data":[{"year":str(y),"period":"M01","value":"1"} for y in range(start,end+1)]}]}}
        with patch.object(cpi,"_fetch_window",side_effect=[window(2014,2023),window(2024,2025)]) as m:
            out=cpi.fetch()
        self.assertEqual([x.args for x in m.call_args_list],[(2014,2023),(2024,2025)])
        self.assertEqual(len(out["Results"]["series"][0]["data"]),12)

    def test_periodic_coverage_for_both_series(self):
        r=parse({"status":"REQUEST_SUCCEEDED","Results":{"series":[rows("CUUR0000SA0",12),rows("CUURS49DSA0",6)]}})
        self.assertEqual(len(r["national_cpi_u"]["values"]),12)
        self.assertEqual(len(r["seattle_cpi_u"]["values"]),12)
        self.assertEqual(r["national_cpi_u"]["expected_periods_per_year"],12)
        self.assertEqual(r["seattle_cpi_u"]["expected_periods_per_year"],6)

    def test_missing_period_fails(self):
        n=rows("CUUR0000SA0",12); s=rows("CUURS49DSA0",6); s["data"]=s["data"][1:]
        with self.assertRaisesRegex(RuntimeError,"expected 6 periodic observations"):
            parse({"status":"REQUEST_SUCCEEDED","Results":{"series":[n,s]}})

if __name__=="__main__":
    unittest.main()
