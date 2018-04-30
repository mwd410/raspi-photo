
def evenFibs(max):
    sum = 0
    fib1 = 1
    fib2 = 0
    for i in range(1, max):
        fibi = fib1 + fib2
        if fibi > max:
            break
        print "i: " + str(i) + " fib: " + str(fibi)
        fib2 = fib1
        fib1 = fibi
        if fibi % 2 == 0:
            sum += fibi
    return sum

print evenFibs(4000000)
