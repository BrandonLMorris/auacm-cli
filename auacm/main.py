"""
main.py

The central entry point of the auacm app.
"""

import requests, sys
import auacm
import auacm.utils as utils
import auacm.user

def main(args):
    """
    Entry point for the auacm-cli app

    Supported commands (passed as positional arguments):
        [none]      print logo and help
        test        attempt to connect to the server
        login       log in as a user to the website
        logout      log out of current session
        whoami      print basic info about the current user
    """
    try:
        if not args or args[0] in {'-h', '--help'}:
            # No subcommand, print info
            print(auacm.logo)
            print('Wecome to the Auburn ACM command-line interface!')
            print(
                'Supported Commands:\n'
                '[none], -h, --help  print this lovely help\n'
                'test                attempt to connect to the server\n'
                'login               log into the website\n'
                'logout              log out of current session\n'
                'whoami              print basic info about the current user')

        elif args[0] in utils.callbacks:
            utils.callbacks[args[0]](args[1:])

        else:
            print('Whoops, that subcommand isn\'t supported.\n'
                  'Run again with -h or --help to see full list of commands.')

    except requests.exceptions.ConnectionError as exception:
        print('There was an error connecting to the server')
        print(exception.message)
        exit(1)

@utils.subcommand('test')
def test(_):
    """Try to connect to the server"""
    test_url = auacm.BASE_URL[:-4]
    response = requests.get(test_url)
    if response.ok:
        print('Connection successful! ' + str(response.status_code))
    else:
        print('Error status code received from the server')


if __name__ == '__main__':
    # Run the app from the main.py script directly
    main(sys.argv[1:])
