import hashlib
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from openpyxl import Workbook

from rsd407_pay.collect import collect_one
from rsd407_pay.sources import Provenance


def s275_xlsx_fixture():
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Districts Q-Z"
    sheet.append(
        [
            "School District",
            "Name",
            "Duty Title",
            "Cert FTE",
            "Clas FTE",
            "Base Salary",
            "Total Salary",
            "Insurance Benefits",
            "Mandatory Benefits",
        ]
    )
    sheet.append(
        [
            "Riverview School District",
            "Fixture Employee",
            "Teacher",
            1.0,
            0.0,
            100000,
            105000,
            16000,
            19000,
        ]
    )
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


class CollectTests(unittest.TestCase):
    def test_collect_writes_hash_matched_immutable_file(self):
        payload = s275_xlsx_fixture()
        provenance = Provenance(
            "2024-25",
            "https://ospi.k12.wa.us/safs-data-files",
            "https://ospi.k12.wa.us/a.xlsx",
            "xlsx",
        )

        def validated(obj):
            obj.sha256 = hashlib.sha256(payload).hexdigest()
            obj.byte_size = len(payload)
            obj.retrieved_at = "now"
            obj.http_status = 200
            obj.content_type = "application/octet-stream"
            return obj

        with (
            tempfile.TemporaryDirectory() as td,
            patch(
                "rsd407_pay.collect.validate_download",
                side_effect=validated,
            ),
            patch(
                "rsd407_pay.collect.fetch",
                return_value=(
                    payload,
                    {"final_url": provenance.direct_download_url},
                ),
            ),
        ):
            row = collect_one(provenance, Path(td))
            self.assertEqual(Path(row["local_path"]).read_bytes(), payload)
            self.assertEqual(
                row["sha256"],
                hashlib.sha256(payload).hexdigest(),
            )
            self.assertEqual(row["workbook_identity"]["format"], "xlsx")
            self.assertEqual(
                row["workbook_identity"]["sheet"],
                "Districts Q-Z",
            )


if __name__ == "__main__":
    unittest.main()
