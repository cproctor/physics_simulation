E = 2.71828

def make_sigmoid(midpoint, steepness):
    "this is a function which builds the desired sigmoid function"
    def inverted_sigmoid(x):
        return 1 - (1 / (1 + E ** (-steepness * (x - midpoint))))
    return inverted_sigmoid

def make_exponential(steepness):
    def exponential(x):
        return max(0, steepness * E ** (-steepness * x))
    return exponential
    
