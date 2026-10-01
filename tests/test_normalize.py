import unittest

from rsd407_pay.normalize import canonicalize_row, header_positions, is_riverview


class NormalizeTests(unittest.TestCase):
    def test_preserves_duplicate_header_positions(self):
        self.assertEqual(header_positions(["Cert #", "Name", "Cert #"])["cert #"], [0, 2])

    def test_canonicalizes_core_fields_and_provenance(self):
        headers = ["School District", "Duty Title", "Cert FTE", "Clas FTE", "Base Salary", "Total Salary"]
        source = ["Riverview School District", "Teacher", 1, 0, "$100,000", "105000"]
        row = canonicalize_row(
            school_year="2024-25", source_sha256="abc", source_sheet="Q-Z",
            source_row=42, headers=headers, row=source,
        )
        self.assertEqual(row["district_name"], "Riverview School District")
        self.assertEqual(row["certificated_fte"], 1.0)
        self.assertEqual(row["base_salary"], 100000.0)
        self.assertEqual(row["source_row"], 42)
        self.assertEqual(row["source_sha256"], "abc")

    def test_duplicate_certificate_uses_first_nonempty_position(self):
        headers = ["Cert #", "Name", "Cert #"]
        row = canonicalize_row(
            school_year="2013-14", source_sha256="abc", source_sheet="A-G",
            source_row=2, headers=headers, row=["", "Person", "CERT123"],
        )
        self.assertEqual(row["certificate_number"], "CERT123")

    def test_class_fte_alias(self):
        row = canonicalize_row(
            school_year="2013-14", source_sha256="abc", source_sheet="A-G",
            source_row=2, headers=["Class FTE"], row=[0.75],
        )
        self.assertEqual(row["classified_fte"], 0.75)

    def test_riverview_filter_is_exact_normalized_district_name(self):
        self.assertTrue(is_riverview({"district_name": " Riverview   School District "}))
        self.assertFalse(is_riverview({"district_name": "Riverview"}))
        self.assertFalse(is_riverview({"district_name": "Other School District"}))


if __name__ == "__main__":
    unittest.main()
