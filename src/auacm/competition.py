"""Subcommands related to competitions"""

import auacm, requests, textwrap
from datetime import datetime
from auacm.utils import subcommand
from auacm.exceptions import CompetitionNotFoundError

@subcommand('competition')
@subcommand('competitions')
def get_comps(args=None):
    """Retrieve one or more competitions from the server"""
    if args:
        return _get_one_comp(args)

    response = requests.get(auacm.BASE_URL + 'competitions')

    comps = response.json()['data']
    current = _format_comps(comps['ongoing'])
    upcoming = _format_comps(comps['upcoming'])
    past = _format_comps(comps['past'])

    return textwrap.dedent('''
        [AUACM Competitions]

        Current
        =======
        {}

        Upcoming
        ========
        {}

        Past
        ====
        {}
        ''').format(current, upcoming, past).strip()

def _get_one_comp(args):
    """Retrieve info on one specific competition"""
    response = requests.get(auacm.BASE_URL + 'competitions/' + str(args[0]))

    if not response.ok or response.status_code == 404:
        raise CompetitionNotFoundError(
            'Could not find competition with id: ' + str(args[0]))

    comp = response.json()['data']

    # 3 Sections: competition, teams, problems
    comp_str = _format_comps([comp['competition']])
    teams = _format_teams(comp['teams'])
    problems = _format_problems(comp['compProblems'])

    return textwrap.dedent('''
        {}

        Teams
        =====
        {}

        Problems
        ========
        {}
        ''').format(comp_str, teams, problems)

def _format_comps(comps):
    """Return a formatted string for a list of competitions"""
    result = list()
    for comp in comps:
        result.append('{}\t{}\t{}'.format(
            comp['name'], comp['cid'], _get_start_date(comp['startTime'])))

    return '\n'.join(result)

def _format_teams(teams):
    """Return a formatted string of the teams passed in"""
    result = ''
    for team in teams:
        result += team['name'] + '\n'
        if len(team['users']) > 1:
            for user in team['users']:
                result += '|    ' + user + '\n'
        result += '\n'
    return result.strip()

def _format_problems(probs):
    """Return a formatted string of the problems passed in"""
    result = ''
    for label, prob in probs.items():
        result += '{}\t{} ({})\n'.format(label, prob['name'], prob['pid'])
    return result.strip()

def _get_start_date(start_time):
    """Return a formatted date string from a competition start time"""
    return datetime.fromtimestamp(start_time).strftime('%m-%d-%Y %H:%M:%S')
