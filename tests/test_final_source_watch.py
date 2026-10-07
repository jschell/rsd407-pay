import unittest
from rsd407_pay.final_source_watch import candidates

CONFIG={'landing_page':'https://ospi.k12.wa.us/safs-data-files',
        'allowed_hosts':['ospi.k12.wa.us'], 'expected_final_years':['2024-25']}
HEADER='<html>Personnel Reporting Data S-275 '

class FinalSourceWatchTests(unittest.TestCase):
    def test_new_final_year_is_candidate_without_promoting_it(self):
        html=HEADER+'<a href="/2025-2026_final_school_personnel.xlsx">2025-26 School Personnel Final</a></html>'
        rows=candidates(html,CONFIG)
        self.assertEqual(rows[0]['school_year'],'2025-26')
        self.assertTrue(rows[0]['outside_accepted_years'])
        self.assertEqual(CONFIG['expected_final_years'],['2024-25'])
        self.assertEqual(rows[0]['status'],'candidate_requires_validation')

    def test_preliminary_foreign_invalid_year_and_non_personnel_are_rejected(self):
        for href,label in [('/2025-2026_final_personnel.xlsx','2025-26 Preliminary'),
                           ('https://other.example/2025-2026_final_personnel.xlsx','2025-26 Final'),
                           ('/2025-2027_final_personnel.xlsx','2025-27 Final'),
                           ('/2025-2026_final_expenditures.xlsx','2025-26 Final Expenditures'),
                           ('/2025-2026_final_personnel.pdf','2025-26 Final Personnel')]:
            self.assertEqual(candidates(HEADER+f'<a href="{href}">{label}</a></html>',CONFIG),[])

    def test_finality_and_dataset_identity_are_required(self):
        self.assertEqual(candidates(HEADER+'<a href="/2025-2026_personnel.xlsx">2025-26 Personnel</a>',CONFIG),[])
        with self.assertRaises(RuntimeError):
            candidates('<html><a href="/2025-2026_final_personnel.xlsx">Final</a></html>',CONFIG)
