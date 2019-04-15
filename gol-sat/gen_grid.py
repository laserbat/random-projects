#!/usr/bin/python3
import copy

"""

A B C
D E F
G H I

"""

WIDTH = 16
HEIGHT = 16

#template = open("gol_template.cnf").read()
template = ""
while True:
    try:
        template += input() + "\n"
    except:
        break

def tolin(x):
    r = x[1] + WIDTH * x[0]
    r = (WIDTH * HEIGHT + r) % (WIDTH * HEIGHT)
    return r + 1

for i in range(0, WIDTH):
    for j in range(0, HEIGHT):
        if i < 1 or j < 1 or i >= WIDTH - 1 or j >= HEIGHT - 1:
            print(str(-tolin((i, j))) + " 0")

for i in range(0, WIDTH):
    for j in range(0, HEIGHT):
        out = copy.copy(template)
        A = (i - 1, j - 1)
        B = (i - 1, j)
        C = (i - 1, j + 1)
        D = (i, j - 1)
        E = (i, j)
        F = (i, j + 1)
        G = (i + 1, j - 1)
        H = (i + 1, j)
        I = (i + 1, j + 1)
        
        repl = {}
        repl['A'] = tolin(A)
        repl['B'] = tolin(B)
        repl['C'] = tolin(C)
        repl['D'] = tolin(D)
        repl['E'] = tolin(E)
        repl['F'] = tolin(F)
        repl['G'] = tolin(G)
        repl['H'] = tolin(H)
        repl['I'] = tolin(I)
        
        for key in repl:
            out = out.replace(key, str(repl[key]))

        print(out, end="")
