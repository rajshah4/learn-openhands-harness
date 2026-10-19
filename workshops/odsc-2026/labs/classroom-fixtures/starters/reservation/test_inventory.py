import unittest
from inventory import Inventory
class Smoke(unittest.TestCase):
 def test_one(self):
  x=Inventory({'a':3});self.assertTrue(x.reserve('r',[('a',1)]));self.assertEqual(x.snapshot(),{'a':2})
