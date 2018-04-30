primeList = [2]

def primes(min, max):
    if 2 >= min: yield 2
    for i in xrange(3, max, 2):
        p = 1
        for p in primeList:
            if i % p == 0 or p * p > i: break
        if i % p:
            primeList.append(i)
            if i >= min: yield i

def factors(n):
    for p in primes(2, n):
        if n % p == 0:
            n = n / p
            yield p
        if n == 1: break

print max(factors(600851475143))

