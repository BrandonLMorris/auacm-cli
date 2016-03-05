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
    verbose = True if args and args[0] in {'-v', '--verbose'} else False
    if verbose:
        query = args[1] if len(args) > 1 else ''
    else:
        query = args[0] if args else ''

    # GET request to the API
    request = requests.get(auacm.BASE_URL + 'problems')

    if not request.ok:
        print('There was an error getting the problems')
        return

    # Filter out problems that aren't similar to the query
    problem_data = request.json()['data']
    results = list()
    for problem in problem_data:
        if query.lower() in problem['name'].lower():
            results.append(problem)

    # Print the results
    for result in results:
        print(result['name'])
        if verbose:
            print('    | added: ' + str(result['added']))
            print('    | appeared: ' + result['appeared'])
            print('    | difficulty: ' + str(result['difficulty']))
            print('    | pid: ' + str(result['pid']))
            print('    | shortname: ' + result['shortname'])
            print('    | solved: ' + str(result['solved']))
            print('    | url: ' + result['url'])


@subcommand('problem-info')
def get_problem_info(args):
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
            print('Could not find problem named ' + args.problem)
            exit(1)

    response = requests.get(auacm.BASE_URL +  'problems/ ' + str(pid))

    if not response.ok:
        print('There was an error retrieving the problem')
        if auacm.DEBUG:
            print(response.text)
        exit(1)

    data = response.json()['data']

    # Print all the results
    print(textwrap.dedent('''
        Name: {}

        Description
        {}

        Input
        {}

        Output
        {}
        '''.format(
            data['name'],
            data['description'],
            data['input_desc'],
            data['output_desc']
            )))

    for case in data['sample_cases']:
        print('Sample Case {}'.format(case['case_num']))
        print('Input:')
        print(case['input'])
        print()

        print('Output:')
        print(case['output'])
        print()

