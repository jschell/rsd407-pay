import json
import tempfile
import unittest
from pathlib import Path
from rsd407_pay.period import accepted_years, require_coverage
from rsd407_pay.coverage_gate import check


class PeriodTests(unittest.TestCase):
    def test_invalid_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'sources.json'
            for years in ([], ['2024-26'], ['2024-25', '2024-25'], ['2022-23', '2024-25']):
                path.write_text(json.dumps({'expected_final_years': years}))
                with self.assertRaises(RuntimeError):
                    accepted_years(path)

    def test_duplicate_coverage(self):
        with self.assertRaises(RuntimeError):
            require_coverage([{'school_year':'2024-25'}]*2, ['2024-25'], 'test')

    def test_future_year_requires_all_dependencies(self):
        years = ['2024-25', '2025-26']
        rows = [{'school_year': y} for y in years]
        published = [{'school_year': y, 'review_status': 'accepted'} for y in years]
        cpi = {'series': {name: {'values': {'2025': 100, '2026': 101}}
                         for name in ('national_cpi_u', 'seattle_cpi_u')}}
        collection = {'release_scope':'final', 'sources':rows}
        self.assertEqual(check(collection, {'years':rows}, cpi, {'years':rows},
                               {'years':published}, years)['status'], 'pass')
        report = check(collection, {'years':rows[:1]}, {'series':{}},
                       {'years':rows[:1]}, {'years':published[:1]}, years)
        self.assertEqual(report['status'], 'fail')
        self.assertEqual(len(report['errors']), 5)
        collection['release_scope'] = 'preliminary'
        self.assertIn('S-275 snapshot must be final', check(collection, {'years':rows}, cpi,
                      {'years':rows}, {'years':published}, years)['errors'])
