"""Fake objects for mock testing"""

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
