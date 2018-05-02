import math

def squareOfSum(xs):
    s = sum(xs)
    return s * s

def sumOfSquares(xs):
    return sum(map(lambda x: x * x, xs))

def diff(xs):
    return squareOfSum(xs) - sumOfSquares(xs)


print diff(xrange(1, 101))

