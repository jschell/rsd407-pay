import unittest

from rsd407_pay.duty_inventory import candidate_headers


class DutyInventoryTests(unittest.TestCase):
    def test_surfaces_code_and_assignment_candidates_without_mapping(self):
        headers = ["School District", "Duty Title", "Duty Code", "Assignment Code", "Base Salary"]
        got = candidate_headers(headers)
        self.assertEqual([x["normalized"] for x in got], ["duty title", "duty code", "assignment code"])
        self.assertEqual([x["index"] for x in got], [1, 2, 3])

    def test_does_not_treat_salary_as_code_candidate(self):
        self.assertEqual(candidate_headers(["School District", "Base Salary", "Total Salary"]), [])


if __name__ == "__main__":
    unittest.main()
