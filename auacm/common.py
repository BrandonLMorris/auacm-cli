"""Package level common values"""
import os

DEBUG = False
BASE_URL = 'http://localhost:5000/api/' if DEBUG else 'http://auacm.com/api/'

try:
    session = (open(
            os.path.join(os.path.expanduser('~'), '.auacm_session.txt'), 'r')
            .readline().strip())
except FileNotFoundError as exception:
    session = ''

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
