# auacm-cli

A command line interface to the Auburn ACM web app (auacm.com)

## Installation

### From pip

Run `pip install auacm`

### Build from source

Clone this repository

`git clone https://github.com/brandonlmorris/auacm-cli`

Then in the top-level directroy, run

`python3 setup.py install`

This will install all the code and create the `auacm` shell command.


---

## Usage

`auacm-cli` installs itself as a shell script. In the terminal, run
`$ auacm`
to display the help.

All of the features of `auacm-cli` are written as subcommands to the main
`auacm` script. To log in, run

`$ auacm login`

You will be prompted for your name and password. Your session will be saved,
so you don't need to authenticate with every run of the script. Subcommands
`logout` and `whoami` exist to destroy the current session and print data
about the current user respectively.

### Problems

To view all the problems on the server, run

`$ auacm problem`

(Protip: pipe the result into `less` for your reading pleasure:
`$ auacm problem | less`)

To search for a problem, simply add the query after `problem` (multi-word
queries must be enclosed in quotes):

`$ auacm problem "cash cow"`

Adding a `-v` flag will increase the verbosity of the results, providing
the problem id, shortname, difficult, etc.

To get more detailed information on a specific problem, including the
description, input/output, and sample cases, run the subcommand `problem-info`
with the problem name or id.

`$ auacm problem-info parity`

**Note:** Searching by problem name is done by case-insensitive substrings. If
you search "cow" but another problem contains "cow" and comes first
alphabetically, that other problem will be used.

### Submission

You can also submit solutions to problems using `auacm`. To do so, simply
run the `submit` subcommand, followed by the problem name and the solution
file:

`$ auacm submit "cash cow" solution.py`

Note that if you're submitting a Python solution, you can use the `-p` flag
to indicate the version of Python. The default is Python 3.

`$ auacm submit parity parity.py -p 2`

After you submit, `auacm` will query your submission to obtain the results.

## Competitions

The `competition` subcommand can list competitions, and give a detailed view
of a particular competition. To see all competitions, run

`$ auacm competitions`

To get more info about a specific competition, run the command with the
competition name afterword (multi-word queries need to be enclosed in spaces).

`$ auacm competitions "october 15th"

Similar to problems, you can also search for a competition using it's unique
competition id with the `-i` or `--id` flag.

---

## Bugs? Improvements? Funny jokes?

Send them to me at brandon dot morris95 at gmail dot com, or leave a comment
on this repo. Contributions are warmly welcomed.

