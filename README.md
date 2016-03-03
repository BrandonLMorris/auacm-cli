# auacm-cli

A command line interface to the Auburn ACM web app (auacm.com)

## Installation

Clone this repository

`git clone https://github.com/brandonlmorris/auacm-cli`

Then in the top-level directroy, run

`python3 setup.py install`

This will install all the code and create the `auacm` shell command.

(Note: While not currently supported, in the future this project will be
distributed on `pypi` so that it can be installed with `pip`)


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

To view all the problems on the server, run

`$ auacm problem`

(Protip: pipe the result into `less` for your reading pleasure:
`$ auacm problem | less`)

To search for a problem, simply add the query after `problem` (multi-word
queries must be enclosed in quotes):

`$ auacm problem "cash cow"`


## Questions? Comments? Funny jokes?

Send them to me at brandon dot morris95 at gmail dot com, or leave a comment
on this page. Contributions are warmly welcomed.

