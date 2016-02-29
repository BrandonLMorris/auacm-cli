import auacm

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

def main(*args, **kwargs):
    if not args or args[0] in {'-h', '--help'}:
        # No subcommand, print info
        print(logo)
        print('Wecome to the Auburn ACM command-line interface!')
    else:
        print('Whoops, that subcommand isn\'t supported.\n'
              'Run again with -h or --help to see full list of commands.')
