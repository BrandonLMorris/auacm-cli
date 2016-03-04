"""
submit.py

Module for handling submission logic
"""

import requests
import auacm
import argparse
import time
from auacm.utils import subcommand

RESULTS = {
    'start': 'Running',
    'compile': 'Compile Error',
    'runtime': 'Runtime Error',
    'timeout': 'Timeout',
    'wrong': 'Wrong Answer',
    'good': 'Correct Solution'
}

@subcommand('submit')
def submit(args):
    """Submit a solution"""

    # Some basic argument parsing
    parser = argparse.ArgumentParser(
        add_help=False,
        usage='submit [-p {2,3}] <problem> <file>'
    )
    parser.add_argument('-p', '--python', type=int, choices=[2, 3])
    parser.add_argument('problem')
    parser.add_argument('filename')
    parser.add_argument('-i', '--id', action='store_true')
    args = parser.parse_args(args)


    try:
        submit_file = {'file': open(args.filename, 'rb')}
    except ValueError:
        print('Error: Could not open file')
        exit(1)

    if args.id:
        data = {'pid': args.problem}
    else:
        # Look up the pid from the problem name
        response = requests.get(auacm.BASE_URL + 'problems')
        if not response.ok:
            print('There was an error looking up the problem id')
            exit(1)

        pid = -1
        for problem in response.json()['data']:
            if args.problem.lower() in problem['name'].lower():
                pid = problem['pid']
                break

        if pid == -1:
            print('Could not find a problem with the name ' + args.problem)
            exit(1)
        data = {'pid': pid}

    # Set the python version or default to Python 3
    if args.python:
        data.update({'python': 'py' if args.python == 2 else 'py3'})
    elif args.filename.endswith('.py'):
        # Default to Python 3
        data.update({'python': 'py3'})

    response = requests.post(
        auacm.BASE_URL + 'submit', files=submit_file,
        data=data,
        cookies={'session': auacm.session}
    )

    if not response.ok:
        print('There was an error submitting the solution')
        exit(1)

    print('Successful submit. Getting results...')
    job_id = response.json()['data']['submissionId']
    status = 'start'
    while status == 'start':
        response = requests.get(auacm.BASE_URL + 'submit/' + str(job_id))
        status = response.json()['data']['status']
        print(RESULTS[status])
        time.sleep(1)

