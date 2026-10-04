import unittest
from rsd407_pay.findings import change

class FindingsTests(unittest.TestCase):
    def test_percent_change(self):
        self.assertAlmostEqual(change(100,125),25.0)

if __name__=="__main__":
    unittest.main()
