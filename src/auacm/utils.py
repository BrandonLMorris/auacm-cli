"""Utility functions for AUACM package"""

import requests
from auacm.common import BASE_URL

def log(message):
    """Log a message"""
    print(message)

callbacks = dict()

def subcommand(command):
    """Decorator to register a function as a subcommand"""
    def wrapped(function):
        """Add the function to the callbacks"""
        callbacks[command] = function
        return function
    return wrapped


def _find_pid_from_name(name):
    """Look up the pid from the problem name"""
    response = requests.get(BASE_URL + 'problems')
    if not response.ok:
        print('There was an error looking up the problem id')
        exit(1)

    pid = -1
    for problem in response.json()['data']:
        if name.lower() in problem['name'].lower():
            pid = problem['pid']
            break

    return pid

def format_str_len(string, length):
    """Format a string to break before a specified length"""
    words, result, current_line = string.split(), '', 0
    for word in words:
        if current_line + len(word) < length:
            result += ' ' + word
            current_line += 1 + len(word)
        else:
            result += '\n' + word
            current_line = len(word)
    return result

