
primes = [2, 3]

def primeSiev(n):
    j = 0
    # yield cached values
    for p in primes:
        if j >= n: return
        j += 1
        yield p
    i = primes[-1] + 2
    while j < n:
        for p in primes:
            if i % p == 0 or p * p > i: break
        if i % p:
            primes.append(i)
            j += 1
            yield i
        i += 2

def nthPrime(n): return max(primeSiev(n))

print nthPrime(10001)
print nthPrime(3)
