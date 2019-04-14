#!/usr/bin/python3
import random
from os import get_terminal_size
from time import sleep

W,H = get_terminal_size()
H -= 1
 
B=W*H
 
def variables(x, y):
    rotr = lambda y: x>>y|x<<B-y&(1<<B)-1
    p, q = rotr(y), rotr(B-y)
    return p & q, ~(p | q), p ^ q

def transform(x):
    A, E, I = variables(x, 1)
    B, F, J = variables(x, W - 1)
    C, G, K = variables(x, W)
    D, H, L = variables(x, W + 1)

    N = L|x&H
    O = D|x&L

    y  = F&E&(N&C|K&O|x&G&D)
    y |= H&G&(I&B|J&A)
    y |= (I&F|J&E)&(O&G|K&N|H&C)
    y |= (N&G|K&H)&(E&B|F&A|J&I)
 
    return y
 
def out(x):
    out = ""
    for i in range(H):
        for j in range(W):
            out += ".#"[(x >> (j + W * i)) & 1]
        out += "\n"
 
    print(out)
 
data = random.randint(0, 2**B)
 
while True:
    out(data)
    data = transform(data)
    sleep(0.05)
