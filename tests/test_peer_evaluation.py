import unittest
from rsd407_pay.peer_evaluation import decomposition, cost

class EvaluationTests(unittest.TestCase):
 def test_decomposition_preserves_gap_when_rate_offsets_staffing(self):
  a={'central_fte_per_1000_students':2,'central_compensation_per_staff_fte':100,
     'central_compensation':200,'student_fte':1000}
  b={'central_fte_per_1000_students':1,'central_compensation_per_staff_fte':150,
     'central_compensation':150,'student_fte':1000}
  d=decomposition(a,b)
  self.assertEqual(d['staffing_intensity_component']+d['compensation_per_staff_fte_component'],d['total_gap'])
  self.assertGreater(d['staffing_intensity_component'],0)
  self.assertLess(d['compensation_per_staff_fte_component'],0)
 def test_directors_are_only_added_in_explicit_scenario(self):
  r={'central_compensation':200,'director_supervisor_compensation_excluded':300,'student_fte':1000}
  self.assertEqual(cost(r),200)
  self.assertEqual(cost(r,True),500)
