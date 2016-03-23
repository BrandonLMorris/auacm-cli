"""Tests relating to submitting solutions"""

# pylint: disable=invalid-name, no-name-in-module, import-error

import auacm, unittest
from unittest.mock import patch
from mocks import MockResponse, MockFile, PROBLEMS_RESPONSE

class SubmitTests(unittest.TestCase):
    """Tests relating to submits"""

    @patch('builtins.open')
    @patch('requests.get')
    @patch('requests.post')
    def testGoodSubmit(self, mock_post, mock_get, mock_open):
        """A valid submission"""
        mock_open.return_value = MockFile()
        mock_get.side_effect = [
            MockResponse(json=PROBLEMS_RESPONSE),
            MockResponse(json={'data': {'status': 'start'}}),
            MockResponse(json={'data': {'status': 'good'}})]
        mock_post.return_value = MockResponse(
            json={'data': {'submissionId': '0'}})

        result = auacm.submit.submit(['problem 1', 'fake.c'], False)
        self.assertIn('running', result.lower())
        self.assertIn('correct', result.lower())

    @patch('builtins.open')
    def testBadFileSubmit(self, mock_open):
        """Attempt to submit a bad file"""
        mock_open.side_effect = IOError

        self.assertRaises(
            auacm.exceptions.InvalidSubmission,
            auacm.submit.submit, ['problem 1', 'notafile.cpp'])


if __name__ == '__main__':
    unittest.main()

