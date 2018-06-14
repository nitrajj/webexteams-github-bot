import os.path
import unittest
from urlparse import urlparse

from github_bot import githubCommits, toSpark
from mock import patch


class BotTester(unittest.TestCase):
    
    def setUp(self):
        "Starting a Web Server"
        self.port = 8080
        pass

    def test_Signature(self):
        self.assertEqual(githubCommits(), 'okay')

if __name__ == '__main__':
    unittest.main()