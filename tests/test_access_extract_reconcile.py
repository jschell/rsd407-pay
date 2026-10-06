import copy
import unittest
from rsd407_pay.access_extract_reconcile import FIELDS, reconcile
from rsd407_pay.validation import YEARS

class AccessExtractTests(unittest.TestCase):
    def setUp(self):
        self.controls = {'district_code': '17407', 'years': [
            dict(school_year=y, source_sha256='source', database_sha256='db',
                 table='table', **{k: 10 for k in FIELDS}) for y in YEARS]}
        self.metrics = {'district': [dict(school_year=y, **{v: 10 for v in FIELDS.values()}) for y in YEARS]}

    def test_all_measures_and_years_pass(self):
        report = reconcile(self.controls, self.metrics)
        self.assertEqual(report['status'], 'pass')
        self.assertEqual(len(report['years']), 12)

    def test_every_pay_field_and_headcount_is_exact(self):
        for field in FIELDS.values():
            metrics = copy.deepcopy(self.metrics)
            metrics['district'][0][field] += 1
            self.assertEqual(reconcile(self.controls, metrics)['status'], 'fail', field)

    def test_fte_noise_is_separate_from_money_tolerance(self):
        self.metrics['district'][0]['total_fte'] += 5e-7
        self.assertEqual(reconcile(self.controls, self.metrics)['status'], 'pass')
        self.metrics['district'][0]['base_salary'] += 5e-7
        self.assertEqual(reconcile(self.controls, self.metrics)['status'], 'fail')

    def test_missing_duplicate_and_wrong_district_fail(self):
        self.controls['district_code'] = '00000'
        self.assertEqual(reconcile(self.controls, self.metrics)['status'], 'fail')
        self.controls['district_code'] = '17407'
        self.metrics['district'].pop()
        self.assertEqual(reconcile(self.controls, self.metrics)['status'], 'fail')
        self.metrics['district'].append(self.metrics['district'][0])
        self.assertEqual(reconcile(self.controls, self.metrics)['status'], 'fail')
