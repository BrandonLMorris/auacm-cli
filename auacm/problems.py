"""
problems.py

Module for handling problem related commands
"""

import requests
import auacm
from auacm.utils import subcommand

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

