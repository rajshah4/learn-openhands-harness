import unittest
from exporter import export_rows

class ExportTests(unittest.TestCase):
    def test_header(self):
        self.assertTrue(export_rows([]).startswith("customer_id,region"))

if __name__ == "__main__":
    unittest.main()
