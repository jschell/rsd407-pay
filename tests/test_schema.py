import unittest

from rsd407_pay.schema import duplicate_headers, inventory_manifest, schema_family


class SchemaInventoryTests(unittest.TestCase):
    def test_duplicate_headers_are_preserved_and_reported(self):
        headers = ["school district", "cert #", "last name", "cert #"]
        self.assertEqual(duplicate_headers(headers), {"cert #": 2})

    def test_identifies_2022_plus_schema(self):
        headers = [
            "school district", "location code", "building location name", "sex",
            "hispanic", "race", "highest degree", "cert yrs exp",
        ]
        self.assertEqual(schema_family(headers), "2022-plus")

    def test_inventory_requires_validated_identity(self):
        with self.assertRaisesRegex(RuntimeError, "missing workbook_identity"):
            inventory_manifest({"sources": [{"school_year": "2024-25"}]})

    def test_inventory_carries_source_hash(self):
        manifest = {"sources": [{
            "school_year": "2013-14", "sha256": "abc",
            "workbook_identity": {
                "format": "xls", "sheet": "Districts A-G",
                "headers": ["school district", "cert #", "cert #"],
            },
        }]}
        row = inventory_manifest(manifest)["years"][0]
        self.assertEqual(row["sha256"], "abc")
        self.assertEqual(row["duplicate_headers"], {"cert #": 2})


if __name__ == "__main__":
    unittest.main()
