import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from rsd407_pay import normalization_snapshot as ns

class SnapshotTests(unittest.TestCase):
 def test_build_and_verify(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); files=[]
   for i in range(3):
    p=root/f"f{i}"; p.write_bytes(f"x{i}".encode()); files.append(str(p))
   with patch.object(ns,"capture_files",return_value=files):
    m=ns.build("test")
    self.assertEqual(len(m["files"]),3); ns.verify(m)
    Path(files[0]).write_text("changed")
    with self.assertRaisesRegex(RuntimeError,"verification failed"): ns.verify(m)
if __name__=="__main__": unittest.main()


class DynamicCaptureTests(unittest.TestCase):
 def test_capture_uses_declared_cpi_windows(self):
  with tempfile.TemporaryDirectory() as d:
   import os
   previous=Path.cwd()
   try:
    os.chdir(d)
    path=Path("artifacts/normalization/cpi.json")
    path.parent.mkdir(parents=True)
    raw=["artifacts/normalization/raw/bls-cpi-2014-2023.json", "artifacts/normalization/raw/bls-cpi-2024-2026.json"]
    path.write_text(json.dumps({"raw_source_files":raw}))
    self.assertEqual(ns.capture_files(), raw+ns.FILES)
    for invalid in ([raw[0],raw[0]], ["../outside.json"], []):
     path.write_text(json.dumps({"raw_source_files":invalid}))
     with self.assertRaises(RuntimeError): ns.capture_files()
   finally: os.chdir(previous)
