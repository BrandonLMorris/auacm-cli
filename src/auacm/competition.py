"""Subcommands related to competitions"""

import auacm, requests, textwrap, argparse
from datetime import datetime
from auacm.utils import subcommand
from auacm.exceptions import CompetitionNotFoundError

@subcommand('competition')
@subcommand('competitions')
def get_comps(args=None):
    """Retrieve one or more competitions from the server"""
    if args:
        return get_one_comp(args)

    response = requests.get(auacm.BASE_URL + 'competitions')

    # Prettify all the competitions
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

def get_one_comp(args):
    """Retrieve info on one specific competition"""
    parser = argparse.ArgumentParser(
        add_help=False,
        usage='competition [-i/--id] <competition>'
    )
    parser.add_argument('-i', '--id', action='store_true')
    parser.add_argument('competition')
    args = parser.parse_args(args)

    if not args.id:
        # Look up the competition by name
        cid = _cid_from_name(args.competition)
        if cid == -1:
            raise CompetitionNotFoundError(
                'Could not find a competition with the name ' +
                args.competition)
    else:
        cid = args.competition

    response = requests.get(auacm.BASE_URL + 'competitions/' + str(cid))

    if not response.ok or response.status_code == 404:
        raise CompetitionNotFoundError(
            'Could not find competition with id: ' + str(args.competition))

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


@subcommand('score')
@subcommand('scoreboard')
def get_scoreboard(args=None):
    """Get the scoreboard from a competition"""
    parser = argparse.ArgumentParser(
        add_help=False,
        usage='scoreboard [-i/--id] [<competition>]'
    )
    parser.add_argument('-i', '--id', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-p', '--problems', action='store_true')
    parser.add_argument('competition', nargs='?', default='')
    args = parser.parse_args(args)

    # Get the competition id
    if not args.competition:
        # Default to the most recent competition (greatest cid)
        comps = requests.get(auacm.BASE_URL + 'competitions').json()['data']
        cid = -1
        for comp in comps['upcoming'] + comps['ongoing'] + comps['past']:
            cid = max(cid, comp['cid'])

    elif args.id:
        cid = args.competition

    else:
        cid = _cid_from_name(args.competition)

    if cid == -1:
        raise CompetitionNotFoundError(
            'No competition found: ' + args.competition)

    response = requests.get(auacm.BASE_URL + 'competitions/' + str(cid))
    if not response.ok or response.status_code == 404:
        raise CompetitionNotFoundError(
            'Could not find competition with id: ' + str(cid))

    # Parse the response to gather the teams and ranking
    competition = response.json()['data']
    teams = list()
    for team in competition['teams']:
        _team = {'name': team['name'], 'correct': 0, 'time': 0}

        # Tally the team solve count and total time
        for prob in team['problemData'].items():
            prob = prob[1]
            if prob['status'] == 'correct':
                _team['correct'] += 1
                _team['time'] += int(prob['submitTime'])

                # Account for penalty time
                if int(prob['submitCount']) > 1:
                    _team['time'] += 20 * (int(prob['submitCount']) - 1)
        teams.append(_team)

    # Sort the teams first by ranking, than by total time
    teams.sort(key=lambda t: (-t['correct'], t['time']))

    # Build up the response string
    teams_str = ''
    for i in range(len(teams)):
        teams_str += '{}\t{}\t{}\t{}\n'.format(
            i+1,
            # Cut long names short
            (teams[i]['name'] + ' ' * 15)[:15],
            teams[i]['correct'],
            teams[i]['time'])

    result = textwrap.dedent("""
        [{}]

        Rank\tTeam\t\tSolved\tTime
        ====\t====\t\t======\t====
        {}""").format(competition['competition']['name'], teams_str).strip()

    # Handle problem parsing if asked for
    # TODO: Refactor into a function
    if args.problems or args.verbose:
        problems_str = ''

        # Iterate through as as (pid, data_dictionary) tuples
        for problem in competition['compProblems'].items():
            problems_str += problem[0] + ': ' + problem[1]['name'] + '\n'
            pid = str(problem[1]['pid'])

            for team in competition['teams']:
                # Add a team's submit time if they got it right
                submit_time = team['problemData'][pid]['submitTime']

                if submit_time != 0:
                    # Account for penalty time
                    penalty = 20 * int(team['problemData'][pid]['submitCount'])
                    penalty -= 20

                    problems_str += '|\t{}: {}'.format(
                        team['name'],
                        team['problemData'][pid]['submitTime'])

                    # Add penaly if any
                    problems_str += ('(' + str(penalty) + ')\n' if penalty != 0
                                     else '\n')

        result += '\n\n' + problems_str

    return result


def _cid_from_name(comp_name):
    """Return the competition of an id based on it's name"""
    comps = requests.get(auacm.BASE_URL + 'competitions').json()['data']
    for comp in comps['upcoming'] + comps['ongoing'] + comps['past']:
        if comp_name.lower() in comp['name'].lower():
            return int(comp['cid'])

    return -1


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
    for label, prob in sorted(probs.items()):
        result += '{}\t{} ({})\n'.format(label, prob['name'], prob['pid'])
    return result.strip()


def _get_start_date(start_time):
    """Return a formatted date string from a competition start time"""
    return datetime.fromtimestamp(start_time).strftime('%m-%d-%Y %H:%M:%S')

