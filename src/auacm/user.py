"""
user.py

Module for handling user related commands
"""

import requests, getpass, os
import auacm
from auacm import utils


@utils.subcommand('whoami')
def whoami(*args):
    """Return basic info about the currently logged in user"""
    r = requests.get(auacm.BASE_URL + 'me', cookies={'session': auacm.session})
    if r.ok:
        print('User info:')
        for key, val in r.json()['data'].items():
            print('    |{} => {}'.format(key, val))
    else:
        print('There was an error. Are you logged in?' if not auacm.DEBUG else
                'ERROR\n' + r.text)
        exit(1)


@utils.subcommand('logout')
def logout(*args):
    """Log the user out of the current session"""
    open(os.path.join(os.path.expanduser('~'), '.auacm_session.txt'), 'w').close()
    auacm.session = ''


@utils.subcommand('login')
def login(*args):
    """Log a user in to the website. Keeps up with session data"""
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    r = requests.post(auacm.BASE_URL + 'login',
            data={'username': username, 'password': password})

    if r.ok:
        print('Success!')
    else:
        utils.log('There was an error attempting to log in')
        exit(1)

    # Save the new session to a file
    auacm.session = r.cookies['session']
    f = open(os.path.join(os.path.expanduser('~'), '.auacm_session.txt'), 'w')
    f.write(auacm.session + '\n')
    f.close()
