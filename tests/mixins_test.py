import unittest
import unittest_adapter
from app_settings.mixins import FileMixin

class test_mixins(unittest.TestCase):
    
    def test_load(self):
        self.assertEqual(1,1)

if __name__ == "__main__":
    unittest.main()

