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

        self.assertIn('upcoming fake mock', result.lower())
        self.assertIn('ongoing fake mock', result.lower())
        self.assertIn('past fake mock', result.lower())

    @patch('requests.get')
    def testGetOneCompetitionById(self, mock_get):
        """Successfully get one competition by its id"""
        mock_get.return_value = MockResponse(json=COMPETITION_DETAIL)

        result = auacm.competition.get_comps(['-i', '2'])

        self.assertIn('ongoing fake mock', result.lower())
        self.assertIn('fake problem a', result.lower())
        self.assertIn('brando the mando', result.lower())

    @patch('requests.get')
    def testGetOneCompetitionByName(self, mock_get):
        """Successfully get one competition by its name"""
        mock_get.side_effect = [
            MockResponse(json=COMPETITIONS_RESPONSE),
            MockResponse(json=COMPETITION_DETAIL)]

        result = auacm.competition.get_comps(['ongoing'])

        self.assertIn('ongoing fake mock', result.lower())
        self.assertIn('fake problem a', result.lower())
        self.assertIn('brando the mando', result.lower())

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


class ScoreboardTests(unittest.TestCase):
    """Tests related to the scoreboard"""

    @patch('requests.get')
    def testGetScoreboardGood(self, mock_get):
        """Get a valid scoreboard from a competition"""
        mock_get.return_value = MockResponse(json=COMPETITION_DETAIL)

        result = auacm.competition.get_scoreboard(['-i', '2'])
        self.assertIn(('brando the mando' + ' ' * 15)[:15], result.lower())
        self.assertIn('rank', result.lower())
        self.assertIn('solved', result.lower())
        self.assertIn('time', result.lower())

    @patch('requests.get')
    def testGetScoreboardBad(self, mock_get):
        """Attepmpt toget a scoreboard from a comeptition that doesn't exist"""
        mock_get.side_effect = [
            MockResponse(json=COMPETITIONS_RESPONSE), MockResponse(ok=False)]

        self.assertRaises(
            auacm.exceptions.CompetitionNotFoundError,
            auacm.competition.get_scoreboard, ['electric boogaloo'])

    @patch('requests.get')
    def testGetScoreboardWithProblems(self, mock_get):
        """Get a scoreboard with the problem statuses"""
        mock_get.side_effect = [
            MockResponse(json=COMPETITIONS_RESPONSE),
            MockResponse(json=COMPETITION_DETAIL)]

        result = auacm.competition.get_scoreboard(['-v', 'ongoing'])

        self.assertIn('A: Fake Problem A', result)
        self.assertIn('Brando The Mando: 10', result)



if __name__ == '__main__':
    unittest.main()
