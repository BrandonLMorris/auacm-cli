"""
main.py

The central entry point of the auacm app.
"""

import requests, getpass, sys, os
try:
    import auacm
except:
    # If running standalone, need to manually add to the system path
    sys.path.append(os.path.abspath('..'))
    import auacm

def main(*args, **kwargs):
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

        elif args[0] == 'test':
            # Try to connect to the server
            test_url = auacm.base_url[:-4]
            r = requests.get(test_url)
            if r.ok:
                print('Connection successful! ' + str(r.status_code))
            else:
                print('Error status code received from the server')

        elif args[0] == 'login': login()

        elif args[0] == 'whoami': whoami()

        elif args[0] == 'logout': logout()

        else:
            print('Whoops, that subcommand isn\'t supported.\n'
                  'Run again with -h or --help to see full list of commands.')

    except requests.exceptions.ConnectionError as e:
        print('There was an error connecting to the server')
        exit(1)

def login():
    """Log a user in to the website. Keeps up with session data"""
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    r = requests.post(auacm.base_url + 'login',
            data={'username': username, 'password': password})

    if r.ok:
        print('Success!')
    else:
        auacm.log('There was an error attempting to log in')
        exit(1)

    # Save the new session to a file
    auacm.session = r.cookies['session']
    f = open('.session', 'w')
    f.write(auacm.session + '\n')
    f.close()

def whoami():
    """Return basic info about the currently logged in user"""
    r = requests.get(auacm.base_url + 'me', cookies={'session': auacm.session})
    if r.ok:
        print('\n'.join(['{} => {}'
            .format(key, val) for key, val in r.json()['data'].items()]))
    else:
        print('There was an error. Are you logged in?')
        exit(1)

def logout():
    """Log the user out of the current session"""
    open('.session', 'w').close()
    auacm.session = ''


if __name__ == '__main__':
    """Run the app from the main.py script directly"""
    main(*sys.argv[1:])
