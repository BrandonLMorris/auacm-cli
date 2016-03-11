"""Tests related to competitions"""

# pylint: disable=invalid-name, import-error, no-name-in-module

import unittest, auacm
from mocks import MockResponse, COMPETITIONS_RESPONSE, COMPETITION_DETAIL
from unittest.mock import patch

class CompetitionTests(unittest.TestCase):
    """Tests related to competitions"""

    @patch('requests.get')
    def testGetAllCompetitons(self, mock_get):
        """Successfully get all the competitions"""
        mock_get.return_value = MockResponse(json=COMPETITIONS_RESPONSE)

        result = auacm.competition.get_comps()

        self.assertTrue('upcoming fake mock' in result.lower())
        self.assertTrue('ongoing fake mock' in result.lower())
        self.assertTrue('past fake mock' in result.lower())

    @patch('requests.get')
    def testGetOneCompetitionById(self, mock_get):
        """Successfully get one competition by its id"""
        mock_get.return_value = MockResponse(json=COMPETITION_DETAIL)

        result = auacm.competition.get_comps(['-i', '2'])

        self.assertTrue('ongoing fake mock' in result.lower())
        self.assertTrue('fake problem a' in result.lower())
        self.assertTrue('brando the mando' in result.lower())

    @patch('requests.get')
    def testGetOneCompetitionByName(self, mock_get):
        """Successfully get one competition by its name"""
        mock_get.side_effect = [
            MockResponse(json=COMPETITIONS_RESPONSE),
            MockResponse(json=COMPETITION_DETAIL)]

        result = auacm.competition.get_comps(['ongoing'])

        self.assertTrue('ongoing fake mock' in result.lower())
        self.assertTrue('fake problem a' in result.lower())
        self.assertTrue('brando the mando' in result.lower())

    @patch('requests.get')
    def testGetOneCompetitionBadName(self, mock_get):
        """Attempt to get a competition that doesn't exist by name"""
        mock_get.side_effect = [
            MockResponse(json=COMPETITIONS_RESPONSE)]

        self.assertRaises(
            auacm.exceptions.CompetitionNotFoundError,
            auacm.competition.get_comps, ['not real'])

    @patch('requests.get')
    def testGetOneCompetitionBad(self, mock_get):
        """Attempt to get a competition that doesn't exist"""
        mock_get.return_value = MockResponse(ok=False, status_code=404)

        self.assertRaises(
            auacm.exceptions.CompetitionNotFoundError,
            auacm.competition.get_comps, ['-i', '99999999'])


if __name__ == '__main__':
    unittest.main()
