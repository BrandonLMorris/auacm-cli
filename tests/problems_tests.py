"""Tests relating to problems"""

# pylint: disable=invalid-name, no-name-in-module, import-error

import auacm, unittest
from unittest.mock import patch
from mocks import MockResponse, PROBLEMS_RESPONSE, PROBLEM_VERBOSE

class ProblemTests(unittest.TestCase):
    """Tests relating to problems"""

    @patch('requests.get')
    def testGetAllProblems(self, mock_get):
        """Get all the problems with the most basic form of the command"""
        mock_get.return_value = MockResponse(json=PROBLEMS_RESPONSE)

        result = auacm.problems.problems()
        self.assertTrue('Fake Problem 1' in result)
        self.assertTrue('Fake Problem 2' in result)

    @patch('requests.get')
    def testGetProblemByName(self, mock_get):
        """Get a *single* problem by searching with the name"""
        mock_get.return_value = MockResponse(json=PROBLEMS_RESPONSE)

        result = auacm.problems.problems(['1'])
        self.assertEqual(1, len(result.splitlines()))
        self.assertTrue('Fake Problem 1' in result)

    @patch('requests.get')
    def testBadGetProblemName(self, mock_get):
        """Search for a problem (by name) that doesn't exist"""
        mock_get.return_value = MockResponse(json=PROBLEMS_RESPONSE)

        self.assertRaises(
            auacm.exceptions.ProblemNotFoundError,
            auacm.problems.problems, ['not a real problem'])

    @patch('requests.get')
    def testGetProblemById(self, mock_get):
        """Get a *single* problem by searching with the id"""
        mock_get.return_value = MockResponse(json=PROBLEMS_RESPONSE)

        result = auacm.problems.problems(['-i', '2'])
        self.assertEqual(1, len(result.splitlines()))
        self.assertTrue('Fake Problem 2' in result)

    @patch('requests.get')
    def testBadGetProblemId(self, mock_get):
        """Search for a problem (by id) that doesn't exist"""
        mock_get.return_value = MockResponse(json=PROBLEMS_RESPONSE)

        self.assertRaises(
            auacm.exceptions.ProblemNotFoundError,
            auacm.problems.problems, ['-i', '99999999'])

    @patch('requests.get')
    def testProblemVerbose(self, mock_get):
        """Get more data about a problem by specifying verbose"""
        mock_get.side_effect = [
            MockResponse(json=PROBLEMS_RESPONSE),
            MockResponse(json=PROBLEM_VERBOSE)]

        result = auacm.problems.get_problem_info(['problem 1'])
        self.assertTrue('Name: Fake Problem 1' in result)
        self.assertTrue('Input' in result)
        self.assertTrue('Output' in result)
        self.assertTrue('Sample Case 1' in result)


if __name__ == '__main__':
    unittest.main()