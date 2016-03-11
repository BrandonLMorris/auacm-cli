"""
user.py

Module for handling user related commands
"""

import requests, getpass, os
import auacm
from auacm import utils


@utils.subcommand('whoami')
def whoami(args=None):
    """Return basic info about the currently logged in user"""
    r = requests.get(auacm.BASE_URL + 'me', cookies={'session': auacm.session})
    if r.ok:
        return_value = 'User info:\n'
        for key, val in r.json()['data'].items():
            return_value += '    |{} => {}\n'.format(key, val)
        return return_value
    elif r.status_code == 401:
        raise auacm.exceptions.UnauthorizedException('You are not logged in')


@utils.subcommand('logout')
def logout(args=None):
    """Log the user out of the current session"""
    # Erase the contents of the session file
    open(
        os.path.join(os.path.expanduser('~'), '.auacm_session.txt'),
        'w'
    ).close()
    auacm.session = ''


@utils.subcommand('login')
def login(args=None):
    """Log a user in to the website. Keeps up with session data"""
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    response = requests.post(
        auacm.BASE_URL + 'login',
        data={
            'username': username,
            'password': password
        })

    if not response.ok:
        raise auacm.exceptions.ConnectionError(
            'There was an error attempting to log in')

    # Save the new session to a file
    auacm.session = response.cookies['session']
    session_f = open(
        os.path.join(os.path.expanduser('~'), '.auacm_session.txt'),
        'w')
    session_f.write(auacm.session + '\n')
    session_f.close()

    return 'Success!'
