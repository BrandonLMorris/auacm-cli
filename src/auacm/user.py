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
    elif r.status_code == 401:
        raise auacm.exceptions.UnauthorizedException('You are not logged in')


@utils.subcommand('logout')
def logout(*args):
    """Log the user out of the current session"""
    # Erase the contents of the session file
    open(
        os.path.join(os.path.expanduser('~'), '.auacm_session.txt'),
        'w'
    ).close()
    auacm.session = ''


@utils.subcommand('login')
def login(*args):
    """Log a user in to the website. Keeps up with session data"""
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    response = requests.post(
        auacm.BASE_URL + 'login',
        data={
            'username': username,
            'password': password
        })

    if response.ok:
        print('Success!')
    else:
        raise auacm.exceptions.ConnectionError(
            'There was an error attempting to log in')

    # Save the new session to a file
    auacm.session = response.cookies['session']
    session_f = open(
        os.path.join(os.path.expanduser('~'), '.auacm_session.txt'),
        'w')
    session_f.write(auacm.session + '\n')
    session_f.close()
