
def isPythagorean(a, b, c):
    return a * a + b * b == c * c

def findPythagoreanTriplet(sum):
    for i in xrange(1, sum):
        for j in xrange(i + 1, sum - i):
            k = sum - i - j
            print i, j, k
            if isPythagorean(i, j, k):
                return (i, j, k), i * j * k


print findPythagoreanTriplet(12)


