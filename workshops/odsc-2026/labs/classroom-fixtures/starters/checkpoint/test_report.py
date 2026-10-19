import unittest,tempfile,json
from pathlib import Path
from report import build
class ReportSmoke(unittest.TestCase):
 def test_posted_total(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td);(d/'in.csv').write_text('id,amount,status\na,0.10,posted\nb,0.20,posted\np,99.00,pending\na,0.10,posted\n');build(d/'in.csv',d/'out.json');self.assertEqual(json.loads((d/'out.json').read_text()),{'total':'0.30','rows':2})
