import unittest
import githubbot
from githubbot import *

class Test(unittest.TestCase):
 
    def test_add_integers(self):
        self.assertEqual(githubCommits(), "okay")
        return

if __name__ == '__main__':
    unittest.main()