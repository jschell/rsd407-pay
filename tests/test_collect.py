import hashlib, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from rsd407_pay.collect import collect_one
from rsd407_pay.sources import Provenance

class CollectTests(unittest.TestCase):
    def test_collect_writes_hash_matched_immutable_file(self):
        payload=b"x"*2048
        p=Provenance("2024-25","https://ospi.k12.wa.us/safs-data-files","https://ospi.k12.wa.us/a.xlsx","xlsx")
        def validated(obj):
            obj.sha256=hashlib.sha256(payload).hexdigest(); obj.byte_size=len(payload); obj.retrieved_at="now"; obj.http_status=200; obj.content_type="application/octet-stream"; return obj
        with tempfile.TemporaryDirectory() as td, patch("rsd407_pay.collect.validate_download",side_effect=validated), patch("rsd407_pay.collect.fetch",return_value=(payload,{"final_url":p.direct_download_url})):
            row=collect_one(p,Path(td))
            self.assertEqual(Path(row["local_path"]).read_bytes(),payload)
            self.assertEqual(row["sha256"],hashlib.sha256(payload).hexdigest())

if __name__=="__main__": unittest.main()
