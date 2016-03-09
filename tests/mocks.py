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
