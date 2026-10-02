import hashlib, json, tarfile, tempfile, unittest
from pathlib import Path
from rsd407_pay.snapshot import build_snapshot, verify_snapshot

class SnapshotTests(unittest.TestCase):
    def test_build_and_verify(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); raw=root/"artifacts/raw/2024-25"; raw.mkdir(parents=True)
            p=raw/"s275.xlsx"; p.write_bytes(b"source")
            digest=hashlib.sha256(b"source").hexdigest()
            manifests=root/"artifacts/manifests"; manifests.mkdir(parents=True)
            manifest=manifests/"collection.json"
            manifest.write_text(json.dumps({"sources":[{"school_year":"2024-25","local_path":"artifacts/raw/2024-25/s275.xlsx","sha256":digest}]}))
            old=Path.cwd()
            import os
            os.chdir(root)
            try:
                build_snapshot("artifacts/manifests/collection.json","artifacts/raw","snapshot.tar.gz","s275-test")
                self.assertEqual(verify_snapshot()["snapshot_tag"],"s275-test")
            finally: os.chdir(old)
if __name__=="__main__": unittest.main()
