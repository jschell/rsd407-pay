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
   with patch.object(ns,"FILES",files):
    m=ns.build("test")
    self.assertEqual(len(m["files"]),3); ns.verify(m)
    Path(files[0]).write_text("changed")
    with self.assertRaisesRegex(RuntimeError,"verification failed"): ns.verify(m)
if __name__=="__main__": unittest.main()
