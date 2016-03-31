"""
main.py

The central entry point of the auacm app.
"""

import requests, sys, textwrap
import auacm
import auacm.utils as utils
from auacm.exceptions import ConnectionError, ProblemNotFoundError, UnauthorizedException, InvalidSubmission, CompetitionNotFoundError

def main(args):
    """
    Entry point for the auacm-cli app

    Supported commands (passed as positional arguments):
        [none]        print logo and help
        ping          attempt to connect to the server
        login         log in as a user to the website
        logout        log out of current session
        whoami        print basic info about the current user
        problem       search for a problem
        submit        submit a solution to a problem
        problem-info  get detailed information on a problem
    """
    if not args or args[0] in {'-h', '--help'}:
        # No subcommand, print info
        print(auacm.logo)
        print('Wecome to the Auburn ACM command-line interface!')
        print(textwrap.dedent('''
            Supported Commands:
            [none], -h, --help  print this lovely help
            ping                attempt to connect to the server
            login               log into the website
            logout              log out of current session
            whoami              print basic info about the current user
            problem [-v/--verbose] search for a problem
            submit [-i/--id][-p/--python {2, 3}] <problem> <file>
            problem-info [-i/--id] <problem>
            competitions [[-i/--id] <competition>]
            init [-i/--id] <problem>
            test <solution> [[-i/--id] <problem>] [-p/--python {2, 3}]
        '''))

    elif args[0] in utils.callbacks:
        try:
            print(utils.callbacks[args[0]](args[1:]) or '')
        except (ProblemNotFoundError,
                UnauthorizedException,
                InvalidSubmission,
                CompetitionNotFoundError) as exp:
            print(exp.message)
            exit(1)
        except (requests.exceptions.ConnectionError, ConnectionError):
            print('There was an error connecting to the server: {}'
                  .format(auacm.BASE_URL))
            exit(1)

    else:
        print('Whoops, that subcommand isn\'t supported.\n'
              'Run again with -h or --help to see full list of commands.')


@utils.subcommand('ping')
def test(_=None):
    """Try to connect to the server"""
    test_url = auacm.BASE_URL[:-4]
    response = requests.get(test_url)
    if response.ok:
        return 'Connection successful! ' + str(response.status_code)
    else:
        raise auacm.exceptions.ConnectionError('Could not connect to server')


if __name__ == '__main__':
    # Run the app from the main.py script directly
    main(sys.argv[1:])
