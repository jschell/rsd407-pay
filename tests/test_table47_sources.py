import hashlib, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from rsd407_pay.table47_sources import collect

class Table47SourceTests(unittest.TestCase):
    @patch("rsd407_pay.table47_sources.fetch_bytes", return_value=b"%PDF-test")
    def test_retains_pdf_with_hash_and_provenance(self, _fetch):
        inv={"resources":[{"school_year":"2024-25","url":"https://example/report.pdf","label":"report","extension":".pdf","table":"47","source_mode":"embedded"}]}
        with tempfile.TemporaryDirectory() as d:
            r=collect(inv,Path(d)); x=r["resources"][0]
            self.assertEqual(x["sha256"],hashlib.sha256(b"%PDF-test").hexdigest())
            self.assertEqual(Path(x["local_file"]).read_bytes(),b"%PDF-test")
            self.assertEqual(x["table"],"47")
if __name__=="__main__": unittest.main()
