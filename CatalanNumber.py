import math

def catalan(n):
    return math.comb(2*n, n) // (n + 1)

n = int(input("Enter n: "))
print("Catalan number:", catalan(n))
