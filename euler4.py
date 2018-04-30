# TODO: Better way?
def isPalindrome(n):
    return str(n)[::-1] == str(n)

def maxOfDigits(n):
    max = 9
    while n > 1:
        max = max * 10 + 9
        n -= 1
    return max

def minOfDigits(n):
    min = 1
    while n > 1:
        min = min * 10
        n -= 1
    return min

def nDigitProducts(n):
    for i in xrange(maxOfDigits(n), minOfDigits(n), -1):
        for j in xrange(maxOfDigits(n), minOfDigits(n), -1):
            product = i * j
            if isPalindrome(product):
                yield i * j

print max(nDigitProducts(3))

