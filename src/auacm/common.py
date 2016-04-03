"""Package level common values"""
import os, json

DEBUG = False
BASE_URL = 'http://localhost:5000/api/' if DEBUG else 'http://auacm.com/api/'
DATA_FILE = os.path.join(os.path.expanduser('~'), '.auacmrc')

try:
    with open(DATA_FILE) as data:
        session = json.load(data)['session']
except (IOError, ValueError, KeyError):
    session = ''

# pylint: disable=anomalous-backslash-in-string
logo = """
     /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$  /$$      /$$
    /$$__  $$| $$  | $$ /$$__  $$ /$$__  $$| $$$    /$$$
   | $$  \ $$| $$  | $$| $$  \ $$| $$  \__/| $$$$  /$$$$
   | $$$$$$$$| $$  | $$| $$$$$$$$| $$      | $$ $$/$$ $$
   | $$__  $$| $$  | $$| $$__  $$| $$      | $$  $$$| $$
   | $$  | $$| $$  | $$| $$  | $$| $$    $$| $$\  $ | $$
   | $$  | $$|  $$$$$$/| $$  | $$|  $$$$$$/| $$ \/  | $$
   |__/  |__/ \______/ |__/  |__/ \______/ |__/     |__/
"""
