import unittest
from rsd407_pay.peer_comparison import DISTRICTS, aggregate

class PeerTests(unittest.TestCase):
 def test_same_definition_and_excluded_directors(self):
  enrollment={('2024-25',d):{'student_fte':1000,'district_code':d,'source_label':d} for d in DISTRICTS}
  rows=[]
  for i,(district,names) in enumerate(DISTRICTS.items()):
   for j,title in enumerate(['Superintendent','Director/Supervisor']):
    rows.append(dict(district_name=names[0],duty_title=title,source_sheet='staff',source_row=i*2+j,
       certificated_fte=1,classified_fte=0,base_salary=90,total_salary=100,insurance_benefits=10,mandatory_benefits=20))
  result,_=aggregate(rows,enrollment,{'Superintendent':'district/central administration','Director/Supervisor':'other classified'},'2024-25')
  self.assertTrue(all(r['central_compensation_per_1000_students']==130 and r['director_supervisor_fte_excluded']==1 for r in result))
  with self.assertRaisesRegex(RuntimeError,'duplicate'):aggregate(rows+[rows[0]],enrollment,{'Superintendent':'district/central administration','Director/Supervisor':'other classified'},'2024-25')
