import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

#class MyTestCase(unittest.TestCase):
    #def test_something(self):
    #    self.assertEqual(True, False)  # add assertion here

if __name__ == '__main__':
    unittest.main()
