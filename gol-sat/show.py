#!/usr/bin/python3
W = 16
input()
a = input().split(" ")
del a[-1]
a = list(map(lambda x: int(int(x) > 0), a))

out = ""
for i,e in enumerate(a):
    out += ".#"[e]
    if i % W == W - 1:
        out += "\n"

print(out)
