# These are factory functions: they build and return functions.
# Here, they are used to build parametrized versions of functions we'll 
# need for forces.

E = 2.71828

def make_sigmoid(midpoint, steepness):
    """
    The sigmoid function is a useful function which always has a value between 0 and 1, 
    parametrized by the midpoint (where the value is 0.5) and steepness. 
    """
    def inverted_sigmoid(x):
        return 1 - (1 / (1 + E ** (-steepness * (x - midpoint))))
    return inverted_sigmoid

def make_exponential(steepness):
    """
    The exponential function explodes as x increases, parametrized by steepness.
    """
    def exponential(x):
        return max(0, steepness * E ** (-steepness * x))
    return exponential
    
