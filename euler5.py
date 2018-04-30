import sys

check_list = [11, 13, 14, 16, 17, 18, 19, 20]

def isEvenlyDivisible(n, max):
    for i in check_list:
        if n % i:
            return False
    return True

def smallestEvenlyDivisible(max):
    i = 2520
    while i < sys.maxint:
        if isEvenlyDivisible(i, max): return i
        i += 2520

print smallestEvenlyDivisible(20)
