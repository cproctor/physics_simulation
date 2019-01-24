# These are factory functions: they build and return functions.
# Here, they are used to build parametrized versions of functions we'll 
# need for forces.

from random import gammavariate
E = 2.71828

def constant(i):
    "Returns a function which returns a constant. Useful when a function is required, but you just want a constant value."
    return lambda: i

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
    
def sample_dirichlet(alphas):
    """
    Samples the dirichlet distribution, which returns random proportions which sum to 1 and 
    whose expected values are (n0/n, n1/n, n2/n, ...) where n = n0 + n1 + n2 ...
    When alphas are scaled, their expected value does not change. However, larger alphas are
    "heavier," reducing the variance of samples. 
    """
    gammas = [gammavariate(a, 1) for a in alphas]
    gammaSum = sum(gammas)
    return [g/gammaSum for g in gammas]
