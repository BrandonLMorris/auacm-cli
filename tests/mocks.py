"""Fake objects for mock testing"""

PROBLEMS_RESPONSE = {
    'data': [
        {
            "added": 0,
            "appeared": "Not a Competition",
            "comp_release": 0,
            "difficulty": "67",
            "name": "Fake Problem 1",
            "pid": 1,
            "shortname": "fake1",
            "solved": False,
            "url": "problems/fake1/info.pdf"
        },
        {
            "added": 1,
            "appeared": "Almost, but Not Real",
            "comp_release": None,
            "difficulty": "80",
            "name": "Fake Problem 2",
            "pid": 2,
            "shortname": "fake2",
            "solved": True,
            "url": "problems/fake2/info.pdf"
        }
    ]
}

PROBLEM_VERBOSE = {
    "data": {
        "added": 0,
        "appeared": "2010 Southeast",
        "comp_release": 0,
        "description": "This is a fake problem. It's not real.",
        "difficulty": "26",
        "input_desc": "Some numbers and things.",
        "name": "Fake Problem 1",
        "output_desc": "More numbers and such",
        "pid": 1,
        "sample_cases": [
            {
                "case_num": 1,
                "input": "2 2",
                "output": "4"
            }
        ],
        "shortname": "fake1"
    }
}

COMPETITIONS_RESPONSE = {
    'data': {
        'upcoming': [{
            'cid': 1,
            'closed': False,
            'name': 'Upcoming Fake Mock',
            'registered': False,
            'startTime': 0
        }],
        'ongoing': [{
            'cid': 2,
            'closed': False,
            'name': 'Ongoing Fake Mock',
            'registered': False,
            'startTime': 0
        }],
        'past': [{
            'cid': 3,
            'closed': False,
            'name': 'Past Fake Mock',
            'registered': False,
            'startTime': 0
        }]
    }
}

COMPETITION_DETAIL = {
    'data': {
        'compProblems': {
            'A': {
                'name': 'Fake Problem A',
                'pid': 1,
                'shortname': 'fake1'
            }
        },
        'competition': {
            'cid': 2,
            'closed': False,
            'name': 'Ongoing Fake Mock',
            'length': 8,
            'registered': False,
            'startTime': 7
        },
        'teams': [{
            'name': 'Brando The Mando',
            'problemData': {
                '1': {
                    'label': 'A',
                    'status': 'correct',
                    'submitCount': '1',
                    'submitTime': '10'
                }
            },
            'users': ['brandonm']
        }]
    }
}

class MockResponse(object): # pylint: disable=too-few-public-methods
    """Fake response object returned from patched request methods"""
    def __init__(self, **kwargs):
        """Initialize values"""
        self.ok = kwargs.get('ok', True) # pylint: disable=invalid-name
        self.status_code = kwargs.get('status_code', 200)
        self.cookies = kwargs.get('cookies', {})
        self._json = kwargs.get('json', {'data': {}})
        self.text = kwargs.get('text', 'Cogito ergo sum')

    def json(self):
        """Return some fake JSON data"""
        return self._json


class MockFile(object):
    """Fake file-like objects for (not) reading and writing"""
    def write(self, *args):
        """Not actually writing to a file"""
        pass

    def close(self):
        """Not actually closing a file"""
        pass


class MockProcess(object): # pylint: disable=too-few-public-methods
    """Fake External Process"""
    def __init__(self, **kwargs):
        """Create the fake process"""
        self.returncode = kwargs.get('returncode', 0)
        self.return_value = kwargs.get('return_value', '')

    def communicate(self, *args, **kwargs):
        """Simulate feeding input to the process and getting a return value"""
        return (self.return_value, None)

