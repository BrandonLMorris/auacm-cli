"""
submit.py

Module for handling submission logic
"""

import requests
import auacm
from auacm.utils import subcommand

@subcommand('submit')
def submit(args):
    """Submit a solution"""

    if len(args) != 2:
        print('Usage: auacm submit <problem_id> <file>')
        exit(1)

    try:
        submit_file = {'file': open(args[0], 'rb')}
    except ValueError:
        print('Error: Could not open file')
        exit(1)


    # TODO: Add a python field to specify py2/3
    request = requests.post(
        auacm.BASE_URL + 'submit', files=submit_file,
        data={'pid': args[1]},
        cookies={'session': auacm.session}
    )

    if request.ok:
        print('Success!')
    else:
        print('There was an error submitting the solution')
        exit(1)

