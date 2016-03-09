"""
problems.py

Module for handling problem related commands
"""

import requests, argparse, textwrap
import auacm
from auacm.utils import subcommand, _find_pid_from_name

@subcommand('problem')
def problems(args=None):
    """Get all the problems, or search for a specific one"""

    # Some minimal argument parsing
    parser = argparse.ArgumentParser(
        add_help=False,
        usage='problem [-v/--verbose] [-i/--id] <problem>'
    )
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-i', '--id', action='store_true')
    parser.add_argument('problem', nargs='?', default='')
    args = parser.parse_args(args)
    query = args.problem

    # GET request to the API
    request = requests.get(auacm.BASE_URL + 'problems')

    if not request.ok:
        raise auacm.exceptions.ConnectionError(
            'There was an error getting the problems')

    # Filter out problems that aren't similar to the query
    problem_data = request.json()['data']
    results = list()
    for problem in problem_data:
        if not args.id and query.lower() in problem['name'].lower():
            results.append(problem)
        elif args.id and query == str(problem['pid']):
            results.append(problem)

    if not results and query:
        raise auacm.exceptions.ProblemNotFoundError(
            'Could not find problem named {}'.format(query))

    # Print the results
    return_value = ''
    for result in results:
        return_value += result['name'] + '\n'
        if args.verbose:
            return_value += textwrap.dedent("""\
                |    added: {}
                |    appeared: {}
                |    difficulty: {}
                |    pid: {}
                |    shortname: {}
                |    solved: {}
                |    url: {}\n
            """.format(
                result['added'], result['appeared'],
                result['difficulty'], result['pid'],
                result['shortname'], result['solved'], result['url']))

    return return_value.strip()


@subcommand('problem-info')
def get_problem_info(args=None):
    """Get detailed data on a problem (description, input, etc.)"""
    parser = argparse.ArgumentParser(
        add_help=False,
        usage='problem-info [-i/--id] problem'
    )
    parser.add_argument('problem')
    parser.add_argument('-i', '--id', action='store_true')
    args = parser.parse_args(args)

    if args.id:
        pid = args.problem
    else:
        pid = _find_pid_from_name(args.problem)
        if pid == -1:
            raise auacm.exceptions.ProblemNotFoundError(
                'Could not find problem named {}'.format(args.problem))

    response = requests.get(auacm.BASE_URL +  'problems/ ' + str(pid))

    if not response.ok:
        raise auacm.exceptions.ProblemNotFoundError(
            'There was an error getting problem id {}'.format(pid))

    data = response.json()['data']

    # Gather all the results
    return_value = textwrap.dedent('''
        Name: {}

        Description
        {}

        Input
        {}

        Output
        {}
        ''').format(
            data['name'],
            data['description'],
            data['input_desc'],
            data['output_desc']
            )

    for case in data['sample_cases']:
        return_value += textwrap.dedent('''
        Sample Case {}
        Input:
        {}

        Output:
        {}
        ''').format(case['case_num'], case['input'], case['output'])

    return return_value.strip()

