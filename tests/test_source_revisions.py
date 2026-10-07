import hashlib
from pathlib import Path
import tempfile
import unittest
from rsd407_pay.sources import Provenance
from rsd407_pay.source_revisions import check, compare, validate_baseline

class SourceRevisionTests(unittest.TestCase):
    def setUp(self):
        self.body=b'accepted workbook'*100
        self.sha=hashlib.sha256(self.body).hexdigest()
        self.years=['2023-24','2024-25']
        self.baseline={'release_scope':'final','sources':[{'school_year':y,
            'direct_download_url':f'https://ospi.k12.wa.us/{y}.xlsx','sha256':self.sha} for y in self.years]}
        self.candidates=[Provenance(y,'page',f'https://ospi.k12.wa.us/{y}.xlsx','xlsx') for y in self.years]
        self.meta={'status':200,'content_type':'application/octet-stream','final_url':'url'}

    def test_same_url_can_contain_revised_bytes(self):
        before={'sha256':self.sha,'direct_download_url':'same-url'}
        self.assertEqual(compare(before,dict(before,sha256='changed')),'content_revision')
        self.assertEqual(compare(before,dict(before,direct_download_url='new-url')),'url_relocation')

    def test_download_failure_does_not_prevent_later_year_check(self):
        def download(url):
            if '2023-24' in url: raise RuntimeError('first source unavailable')
            return self.body,self.meta
        with tempfile.TemporaryDirectory() as d:
            report=check(self.baseline,self.candidates,self.years,Path(d),fetcher=download,validator=lambda b,f:{'validated':True})
        self.assertEqual(report['status'],'fail')
        self.assertEqual(report['years'][1]['status'],'unchanged')

    def test_revised_bytes_are_preserved_separately_and_corruption_rejected(self):
        revised=self.body+b'revision'
        with tempfile.TemporaryDirectory() as d:
            args=dict(fetcher=lambda url:(revised,self.meta),validator=lambda b,f:{'validated':True})
            report=check(self.baseline,self.candidates,self.years,Path(d),**args)
            self.assertEqual(report['status'],'review_required')
            path=Path(report['years'][0]['revision_local_path'])
            self.assertEqual(path.read_bytes(),revised)
            path.write_bytes(b'corrupt existing evidence')
            repeated=check(self.baseline,self.candidates,self.years,Path(d),**args)
            self.assertEqual(repeated['years'][0]['status'],'check_failed')
            self.assertEqual(path.read_bytes(),b'corrupt existing evidence')

    def test_partial_preliminary_and_duplicate_baselines_are_rejected(self):
        with self.assertRaises(ValueError):validate_baseline(self.baseline,self.years+['2025-26'])
        self.baseline['release_scope']='preliminary'
        with self.assertRaises(ValueError):validate_baseline(self.baseline,self.years)
        self.baseline['release_scope']='final'
        self.baseline['sources'].append(self.baseline['sources'][0])
        with self.assertRaises(ValueError):validate_baseline(self.baseline,self.years)
