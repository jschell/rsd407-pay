import unittest
from rsd407_pay.admin_overhead import build
from rsd407_pay.normalize_metrics import YEARS

class AdminOverheadTests(unittest.TestCase):
 def test_definitions_and_costs(self):
  district=[]; cats=[]; enroll=[]
  for sy in YEARS:
   district.append({"school_year":sy,"reported_employer_compensation":10000})
   cats += [
    {"school_year":sy,"job_family":"district/central administration","total_fte":2,"total_salary":200,"reported_employer_compensation":300},
    {"school_year":sy,"job_family":"principals/APs","total_fte":3,"total_salary":300,"reported_employer_compensation":450}]
   enroll.append({"school_year":sy,"student_fte":1000})
  vals={str(y):100 for y in range(2014,2026)}
  cpi={"series":{n:{"series_id":n,"values":vals} for n in ("national_cpi_u","seattle_cpi_u")}}
  r=build({"district":district,"categories":cats},{"years":enroll},cpi)["years"][0]
  self.assertEqual(r["strict_central_administration"]["employer_compensation_per_student_fte"],.3)
  self.assertEqual(r["strict_central_administration"]["fte_per_1000_student_fte"],2)
  self.assertEqual(r["central_plus_school_administration"]["employer_compensation_per_student_fte"],.75)
  self.assertEqual(r["strict_central_administration"]["share_district_employer_compensation"],.03)
if __name__=="__main__": unittest.main()
