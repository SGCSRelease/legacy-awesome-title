FUNCTIONS = {}


def AddFunction(function):
    """Adding Function Globally."""
    FUNCTIONS[function.__name__] = function
    def _(*args, **kwargs):
        function(*args, **kwargs)
    return _
