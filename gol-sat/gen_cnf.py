#!/usr/bin/python3
import boolexpr as bx
ctx = bx.Context()

a,b,c,d,e,f,g,h,i = map(ctx.get_var, "abcdefghi")


A,B,C,D,E,F,G,H,J,K,L,M = a&b, c&d, e&f, g&h, ~(a|b), ~(c|d), ~(e|f), ~(g|h), a^b, c^d, e^f, g^h

N = M | i & H
O = D | i & M

y=F&E&(N&C|L&O|i&G&D)|(O&G|L&N|H&C)&(J&F|K&E)|(N&G|L&H)&(E&B|F&A|K&J)|H&G&(J&B|K&A)

z = (y & i) | (~y & ~i)

print(z.to_cnf())
