import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from rsd407_pay.revision_impact import DATA, GATES, PROVENANCE, build, compare, load_analysis


def fixture(root):
    snapshots = {'s275':'s275-source-test', 'normalization':'normalization-source-test'}
    payload = {DATA[0]: {'district':[{'school_year':'2024-25','total_fte':4}],
                         'categories':[{'school_year':'2024-25','job_family':'central','total_fte':4}]},
               DATA[1]: {'years':[{'school_year':'2024-25','student_fte':100}]},
               DATA[2]: {'years':[{'school_year':'2024-25','central':{'cost':400}}]},
               DATA[3]: {'source_snapshots':snapshots, 'period':{'start':'2024-25','end':'2024-25'}}}
    payload.update({p:{'status':'pass'} for p in GATES})
    inputs={}
    for path, value in payload.items():
        p=root/path; p.parent.mkdir(parents=True,exist_ok=True)
        data=json.dumps(value).encode(); p.write_bytes(data)
        inputs[path]=hashlib.sha256(data).hexdigest()
    manifest={'gate_status':'pass','analysis_ref':'a'*40,'analysis_run':'123',
              'source_snapshots':snapshots,'period':payload[DATA[3]]['period'],'input_sha256':inputs}
    p=root/PROVENANCE; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(manifest))
    return payload, manifest


class RevisionImpactTests(unittest.TestCase):
    def test_no_change_and_nested_changes_added_year(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); a, _=fixture(root)
            self.assertEqual(compare(a,a), [])
            b=copy.deepcopy(a); b[DATA[2]]['years'][0]['central']['cost']=500
            b[DATA[1]]['years'].append({'school_year':'2025-26','student_fte':120})
            changes=compare(a,b)
            self.assertEqual(len(changes),2)
            money=next(c for c in changes if c['scope']=='administration')
            self.assertEqual(money['difference'],100)
            self.assertEqual(money['percent_change'],25)
            self.assertEqual(next(c for c in changes if c['change_type']=='added')['difference'],None)
            b[DATA[0]]['district']*=2
            with self.assertRaisesRegex(RuntimeError,'duplicate'): compare(a,b)

    def test_hash_and_gate_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); _, manifest=fixture(root)
            (root/DATA[0]).write_text('{}')
            with self.assertRaisesRegex(RuntimeError,'hash mismatch'): load_analysis(root)
            fixture(root)
            data=json.dumps({'status':'fail'}).encode(); (root/GATES[0]).write_bytes(data)
            manifest['input_sha256'][GATES[0]]=hashlib.sha256(data).hexdigest()
            (root/PROVENANCE).write_text(json.dumps(manifest))
            with self.assertRaisesRegex(RuntimeError,'passing gate'): load_analysis(root)

    def test_bundle_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); fixture(root/'before'); fixture(root/'after')
            record=build(root/'before',root/'after',root/'out')
            self.assertEqual(record['changed_measure_count'],0)
            import zipfile
            with zipfile.ZipFile(root/'out/revision-evidence.zip') as z:
                for path, expected in record['evidence_sha256'].items():
                    self.assertEqual(hashlib.sha256(z.read(path)).hexdigest(),expected)
            with self.assertRaises(FileExistsError): build(root/'before',root/'after',root/'out')
