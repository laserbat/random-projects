#!/usr/bin/python3
W = 16
input()
a = input().split(" ")
a = list(map(lambda x: str(-int(x)), a))
print(" ".join(a))
