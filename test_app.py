import unittest
from app import bpsData

b = bpsData()

class bpsDataTest(unittest.TestCase):

    def test_get_url(self):
        """url should be declared"""
        self.assertTrue(b.url)

    def test_get_provinces(self):
        """should have Aceh word in provinces list"""
        self.assertIn('Aceh', b.get_provinces())

if __name__ == "__main__":
    unittest.main()
