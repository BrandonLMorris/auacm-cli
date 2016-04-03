"""
user.py

Module for handling user related commands
"""

import requests, getpass, os, json
import auacm
from auacm import utils
from auacm.common import DATA_FILE


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
    # Erase the session from the data file
    try:
        with open(DATA_FILE) as data:
            user_data = json.load(data)
    except (IOError, ValueError):
        user_data = {}
    user_data.pop('session', None)
    with open(DATA_FILE, 'w') as data:
        json.dump(user_data, data, indent=2)


@utils.subcommand('login')
def login(args=None):
    """Log a user in to the website. Keeps up with session data"""
    # Try to read from ~/.auacmrc
    try:
        with open(DATA_FILE) as data:
            user_data = json.load(data)
    except (IOError, ValueError):
        user_data = {}
    if 'username' not in user_data:
        username = input('Username: ')
    else:
        username = user_data['username']

    if 'password' not in user_data:
        password = getpass.getpass('Password: ')
    else:
        password = user_data['password']

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
    user_data['session'] = auacm.session = response.cookies['session']
    with open(DATA_FILE, 'w') as data:
        json.dump(user_data, data, indent=2)

    return 'Success!'
