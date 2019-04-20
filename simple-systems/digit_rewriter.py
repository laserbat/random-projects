#!/usr/bin/python3

#
# G_z(x) is a family of functions that transform an integer into another integer by
# replacing every digit in z with 1 and every digit not in z with 0.
#
# Dynamic system x_(n+1) = G(M * x_n, z) is Turing complete.
#

# Definition of G
def G(x, z):
    out = 0
    for e in str(x):
        out *= 10
        if int(e) in z:
            out += 1
    return out


# Proof by simulation (rule110)
N = 421
M = set([6,5,3,2,1])
a = 1

# For arbitrary N, M and a it is undecidable if this iteration halts
while a:
    print(a)
    a = G(a * N, M)
