"""Tests for user related functions of auacm"""
# pylint: disable=invalid-name

import unittest, auacm                      # pylint: disable=import-error
from mocks import MockResponse, MockFile
from unittest.mock import patch             # pylint: disable=no-name-in-module, import-error

class ConnectionTest(unittest.TestCase):
    """Test connecting to the server"""

    @patch('requests.get')
    def testConnection(self, mock_get):
        """Successful connection to the server"""
        mock_get.return_value = MockResponse()
        self.assertIn('success', auacm.main.test([]))

    @patch('requests.get')
    def testBadConnection(self, mock_get):
        """Unsuccessful connection to the server"""
        mock_get.return_value = MockResponse(ok=False)
        self.assertRaises(auacm.exceptions.ConnectionError,
                          auacm.main.test, [])


class AuthenticationTest(unittest.TestCase):
    """Test authenticating the user"""

    @patch('builtins.input')
    @patch('getpass.getpass')
    @patch('builtins.open')
    @patch('requests.post')
    def testLogin(self, mock_response, mock_file, mock_pass, mock_input):
        """Successful login"""
        mock_input.return_value = 'Username'
        mock_pass.return_value = 'password'
        mock_file.return_value = MockFile()
        mock_response.return_value = MockResponse(
            cookies={'session': 'Fake session'})

        self.assertIn('success', auacm.user.login([]).lower())
        self.assertEqual('Fake session', auacm.session)

    @patch('builtins.open')
    def testLogout(self, mock_file):
        """Successful logout"""
        mock_file.return_value = MockFile()
        auacm.session = 'SomethingNotEmpty'
        auacm.user.logout([])
        self.assertEqual(0, len(auacm.session))


    @patch('requests.get')
    def testWhoami(self, mock_response):
        """Successful 'whoami'"""
        mock_response.return_value = MockResponse(
            json={'data': {'username': 'test user'}})

        returned = auacm.user.whoami([])
        self.assertIn('username', returned)


if __name__ == '__main__':
    unittest.main()
