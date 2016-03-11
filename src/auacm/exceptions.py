"""Custom exception for auacm-cli"""

class ConnectionError(Exception):
    """Represents a failed attempt to connect to the server"""

    def __init__(self, message):
        super(ConnectionError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ProblemNotFoundError(Exception):
    """Represents a failed attempt to locate a problem on the server"""

    def __init__(self, message):
        super(ProblemNotFoundError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class UnauthorizedException(Exception):
    """Represents trying to access a resource they're unauthorized for"""

    def __init__(self, message):
        super(UnauthorizedException, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class InvalidSubmission(Exception):
    """Represents trying to submit an invalid file"""

    def __init__(self, message):
        super(InvalidSubmission, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class CompetitionNotFoundError(Exception):
    """Represents a failed attempt to locate a competition on the server"""

    def __init__(self, message):
        super(CompetitionNotFoundError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message

