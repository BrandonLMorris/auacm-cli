"""
problems.py

Module for handling problem related commands
"""

import requests, argparse, textwrap, os, string, glob, re
import auacm
from auacm.utils import subcommand, _find_pid_from_name, format_str_len
import subprocess
from subprocess import PIPE, STDOUT
from shlex import split

ALLOWED_EXTENSIONS = ['java', 'c', 'cpp', 'py', 'go']
COMPILE_COMMAND = {
    'java': 'javac {0}.java',
    'py': 'NO COMPILE',
    'py3': 'NO COMPILE',
    'c': 'gcc {0}.c -o {0}',
    'cpp': 'g++ {0}.cpp -o {0}',
    'go': 'go build -o {0} {0}.go'
}
RUN_COMMAND = {
    'java': 'java -cp {0} {1}',
    'py3': 'python2.7 {0}/{1}.py',
    'py': 'python3 {0}/{1}.py',
    'c': '{0}/{1}',
    'cpp': '{0}/{1}',
    'go': '{0}/{1}'
}

@subcommand('problem')
def problems(args=None):
    """Get all the problems, or search for a specific one"""

    # Some minimal argument parsing
    parser = argparse.ArgumentParser(
        add_help=False,
        usage='problem [-v/--verbose] [-i/--id] <problem>'
    )
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-i', '--id', action='store_true')
    parser.add_argument('problem', nargs='?', default='')
    args = parser.parse_args(args)
    query = args.problem

    # GET request to the API
    request = requests.get(auacm.BASE_URL + 'problems')

    if not request.ok:
        raise auacm.exceptions.ConnectionError(
            'There was an error getting the problems')

    # Filter out problems that aren't similar to the query
    problem_data = request.json()['data']
    results = list()
    for problem in problem_data:
        if not args.id and query.lower() in problem['name'].lower():
            results.append(problem)
        elif args.id and query == str(problem['pid']):
            results.append(problem)

    if not results and query:
        raise auacm.exceptions.ProblemNotFoundError(
            'Could not find problem named {}'.format(query))

    # Print the results
    return_value = ''
    for result in results:
        return_value += result['name'] + '\n'
        if args.verbose:
            return_value += textwrap.dedent("""\
                |    added: {}
                |    appeared: {}
                |    difficulty: {}
                |    pid: {}
                |    shortname: {}
                |    solved: {}
                |    url: {}\n
            """.format(
                result['added'], result['appeared'],
                result['difficulty'], result['pid'],
                result['shortname'], result['solved'], result['url']))

    return return_value.strip()


@subcommand('problem-info')
def get_problem_info(args=None):
    """Get detailed data on a problem (description, input, etc.)"""
    parser = argparse.ArgumentParser(
        add_help=False,
        usage='problem-info [-i/--id] problem'
    )
    parser.add_argument('problem')
    parser.add_argument('-i', '--id', action='store_true')
    args = parser.parse_args(args)

    if args.id:
        pid = args.problem
    else:
        pid = _find_pid_from_name(args.problem)
        if pid == -1:
            raise auacm.exceptions.ProblemNotFoundError(
                'Could not find problem named {}'.format(args.problem))

    response = requests.get(auacm.BASE_URL +  'problems/ ' + str(pid))

    if not response.ok:
        raise auacm.exceptions.ProblemNotFoundError(
            'There was an error getting problem id {}'.format(pid))

    data = response.json()['data']

    # Gather all the results
    return_value = textwrap.dedent('''
        Name: {}

        Description
        {}

        Input
        {}

        Output
        {}
        ''').format(
            data['name'],
            format_str_len(data['description'], 80),
            format_str_len(data['input_desc'], 80),
            format_str_len(data['output_desc'], 80)
            )

    for case in data['sample_cases']:
        return_value += textwrap.dedent('''
        Sample Case {}
        Input:
        {}

        Output:
        {}
        ''').format(case['case_num'], case['input'], case['output'])

    return return_value.strip()


@subcommand('init')
def init_problem_directory(args=None):
    """Create an initial directory and files for a problem"""
    parser = argparse.ArgumentParser(
        add_help=False,
        usage='init [-i/--id] problem'
    )
    parser.add_argument('problem')
    parser.add_argument('-i', '--id', action='store_true')
    args = parser.parse_args(args)

    if args.id:
        pid = args.problem
    else:
        pid = _find_pid_from_name(args.problem)

    if pid == -1:
        raise auacm.exceptions.ProblemNotFoundError(
            'Could not find problem: ' + args.problem)

    response = requests.get(auacm.BASE_URL + 'problems/' + str(pid))
    if not response.ok:
        raise auacm.exceptions.ProblemNotFoundError(
            'There was an error getting problem id {}'.format(pid))

    data = response.json()['data']

    # Save everything to files
    dir_name = string.capwords(data['name']).replace(' ', '')
    os.mkdir(dir_name)

    desc_file = open(os.path.join(dir_name, 'description.md'), 'w')
    desc_file.write(get_problem_info(['-i', str(pid)]))
    desc_file.close()

    os.mkdir(os.path.join(dir_name, 'tests'))
    for case in data['sample_cases']:
        in_file = open(os.path.join(os.path.join(
            dir_name, 'tests', 'in' + str(case['case_num']) + '.txt')), 'w')
        in_file.write(case['input'])
        in_file.close()

        out_file = open(os.path.join(os.path.join(
            dir_name, 'tests', 'out' + str(case['case_num']) + '.txt')), 'w')
        out_file.write(case['output'])
        out_file.close()

    return 'Done!'


@subcommand('test')
def test_solution(args=None):
    """Run a solution against sample cases"""
    parser = argparse.ArgumentParser(
        add_help=False,
        usage='test [-p {2,3}] <solution> [-i [<problem>]]'
    )
    parser.add_argument('-p', '--python', type=int, choices=[2, 3])
    parser.add_argument('solution')
    parser.add_argument('-i', '--id', action='store_true')
    parser.add_argument('-l', '--local', action='store_true')
    parser.add_argument('problem', nargs='?', default=None)
    args = parser.parse_args(args)


    # Make sure that we can support this filetype
    if not args.solution.split('.')[1] in ALLOWED_EXTENSIONS:
        raise Exception('Filetype not supported')

    # Get the sample cases for the problem
    solution_name = args.solution.split('/')[-1]
    cases = (_get_remote_sample_cases(args.problem, solution_name, args.id) if
             not args.local else _get_local_sample_cases())

    # Compile the solution, if necessary
    compiled = _compile(args.solution, args.python == 3)
    if not compiled: return 'Compilation error'

    filename, filetype = args.solution.split('.')
    if filetype == 'py' and not args.python or args.python == 3:
        filetype = 'py3'
    run_cmd = RUN_COMMAND[filetype].format(os.getcwd(), filename)

    for case in cases:
        # Execute the test solution
        proc = subprocess.Popen(
            split(run_cmd),
            stdout=PIPE,
            stdin=PIPE,
            stderr=STDOUT,
            universal_newlines=True)
        result = proc.communicate(input=case['input'])[0]
        if proc.returncode != 0:
            return 'Runtime error\n' + str(result)

        # Compare the results to the solution
        result_lines = result.splitlines()
        answer_lines = case['output'].splitlines()
        if len(result_lines) != len(answer_lines):
            return textwrap.dedent("""
                Wrong number of lines
                Expected {} line(s)
                Found {} line(s)
                """).strip().format(len(answer_lines), len(result_lines))

        for i in range(len(result_lines)):
            if result_lines[i] != answer_lines[i]:
                return textwrap.dedent("""
                    Wrong answer
                    Expected: {}
                    Found: {}""").strip().format(answer_lines[i],
                                                 result_lines[i])

    return 'Passed all sample cases'


def _compile(solution, py2=False):
    """Attempt to compile a solution, return True if successful"""
    filename, filetype = solution.split('.')
    if COMPILE_COMMAND[filetype] == 'NO COMPILE': return True

    # Execute compilation and return success
    return subprocess.call(
        split(COMPILE_COMMAND[filetype].format(filename))) == 0


def _get_remote_sample_cases(problem, solution, is_id):
    """
    Retrieve the sample cases from the server for a problem for local testing.

    :param problem: The problem name to get the test cases for, or None
    :param solution: the file name of the local solution, if problem is None
    :param is_id: True if the problem argument
    :throws auacm.exceptions.ProblemNotFoundError: if cannot locate the problem
    """
    if problem:
        if is_id:
            pid = int(problem)
        else:
            pid = _find_pid_from_name(problem)
    else:
        # Get the problem name from the solution file
        pid = _find_pid_from_name(solution.split('.')[0])

    if pid == -1:
        raise auacm.exceptions.ProblemNotFoundError(
            'Could not frind problem: ' +
            problem or solution.split('.')[0])


    response = requests.get(auacm.BASE_URL + 'problems/' + str(pid))
    return response.json()['data']['sample_cases']

def _get_local_sample_cases():
    """Retrieve the sample cases locally from the tests/ directory"""
    test_dir = os.path.join(os.getcwd(), 'tests')
    in_files = glob.glob(os.path.join(test_dir, 'in*'))

    if not in_files:
        raise Exception('No test cases found in tests/ directory')

    cases = list()
    for in_file in in_files:
        # Find the corresponding output file
        match = re.search(r'in(\d+).txt', in_file)
        if not match:
            raise Exception('Test files not properly named.'
                            'Should be in1.txt, in2.txt, ...')
        test_num = match.group(1)
        out_file = os.path.join(test_dir, 'out' + test_num + '.txt')

        with open(out_file, 'r') as out_f, open(in_file, 'r') as in_f:
            cases.append({
                'input': in_f.read() + '\n',
                'output': out_f.read()
            })

    return cases

