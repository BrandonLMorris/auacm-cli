import unittest, auacm
from unittest.mock import patch

class ConnectionTestTest(unittest.TestCase):
    @patch('requests.get')
    def test_tests(self, mock_get):
        mock_get.return_value = MockResponse()
        self.assertTrue('success' in auacm.main.test([]))


class MockResponse(object):
    def __init__(self, **kwargs):
        self.ok = kwargs.get('ok', True)
        self.status_code = kwargs.get('status_code', 200)
