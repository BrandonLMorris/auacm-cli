"""Utility function for AUACM package"""

# from auacm import DEBUG

def log(message):
    """Log a message"""
    print(message)

callbacks = dict()

def subcommand(command):
    """Decorator to register a function as a subcommand"""
    def wrapped(function):
        """Add the function to the callbacks"""
        callbacks[command] = function
    return wrapped
