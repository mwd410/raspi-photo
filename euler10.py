
primes = [2, 3]

def primesF(f):
    j = 0
    # yield cached values
    for p in primes:
        if f(j, p): return
        j += 1
        yield p
    i = primes[-1] + 2
    while True:
        for p in primes:
            if i % p == 0 or p * p > i: break
        if i % p:
            primes.append(i)
            j += 1
            yield i
        i += 2
        if f(j, i): return

def nPrimes(n): return primesF(lambda i, p: i >= n)

def primeRange

print sum(primesF(lambda i, p: p >= 4000000))


