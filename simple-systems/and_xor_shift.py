#!/usr/bin/python3

# If F(a) is any function that can be defined as composition of bitwise XORs, ANDs and left shifts
# Then the dynac system x_(n+1) = F(x_n) is Turing complete

# Proof by simulation (rule110)

a = 1
while a:
    print(bin(a))
    a = a ^ (a << 1) ^ (a & (a << 1)) ^ (a & (a << 1) & (a << 2))
