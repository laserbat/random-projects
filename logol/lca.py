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

def transform(x, y):
    PBA, PNA, POA = variables(x, 1)
    PBB, PNB, POB = variables(x, W - 1)
    PBC, PNC, POC = variables(x, W)
    PBD, PND, POD = variables(x, W + 1)

    NBA, NNA, NOA = variables(y, 1)
    NBB, NNB, NOB = variables(y, W - 1)
    NBC, NNC, NOC = variables(y, W)
    NBD, NND, NOD = variables(y, W + 1)

    Y0 = x
    Y1 = y

    P0 = PNA & PNB & PNC & PND
    N0 = NNA & NNB & NNC & NND

    P8 = PBA & PBB & PBC & PBD
    N8 = NBA & NBB & NBC & NBD

    P1 = PNA & PNB & (PNC & POD | PND & POC) | PNC & PND & (PNA & POB | POA & PNB)
    N1 = NNA & NNB & (NNC & NOD | NND & NOC) | NNC & NND & (NNA & NOB | NOA & NNB)

    P7 = PBA & PBB & (PBC & POD | PBD & POC) | PBC & PBD & (PBA & POB | POA & PBB)
    N7 = NBA & NBB & (NBC & NOD | NBD & NOC) | NBC & NBD & (NBA & NOB | NOA & NBB)

    P2 = PNA & PNB & (PBC & PND | POC & POD | PNC & PBD) |  PNC & PND & (PBA & PNB | POA & POB | PNA & PBB) |\
        ((PNA & POB) | (POA & PNB)) & ((PNC & POD) | (POC & PND))

    N2 = NNA & NNB & (NBC & NND | NOC & NOD | NNC & NBD) |  NNC & NND & (NBA & NNB | NOA & NOB | NNA & NBB) |\
        ((NNA & NOB) | (NOA & NNB)) & ((NNC & NOD) | (NOC & NND))

    P6 = PBA & PBB & (PNC & PBD | POC & POD | PBC & PND) |  PBC & PBD & (PNA & PBB | POA & POB | PBA & PNB) |\
        ((PBA & POB) | (POA & PBB)) & ((PBC & POD) | (POC & PBD))

    N6 = NBA & NBB & (NNC & NBD | NOC & NOD | NBC & NND) |  NBC & NBD & (NNA & NBB | NOA & NOB | NBA & NNB) |\
        ((NBA & NOB) | (NOA & NBB)) & ((NBC & NOD) | (NOC & NBD))

    P3 = PNA & PNB & (PBC & POD | POC & PBD) | PNC & PND & (PBA & POB | POA & PBB) | \
         (PNA & POB | POA & PNB ) & (PBC & PND | POC & POD | PNC & PBD) |  \
         (PNC & POD | POC & PND ) & (PBA & PNB | POA & POB | PNA & PBB)

    N3 = NNA & NNB & (NBC & NOD | NOC & NBD) | NNC & NND & (NBA & NOB | NOA & NBB) | \
         (NNA & NOB | NOA & NNB ) & (NBC & NND | NOC & NOD | NNC & NBD) | \
         (NNC & NOD | NOC & NND ) & (NBA & NNB | NOA & NOB | NNA & NBB)


    P5 = PBA & PBB & (PNC & POD | POC & PND) | PBC & PBD & (PNA & POB | POA & PNB) | \
         (PBA & POB | POA & PBB ) & (PNC & PBD | POC & POD | PBC & PND) | \
         (PBC & POD | POC & PBD ) & (PNA & PBB | POA & POB | PBA & PNB)

    N5 = NBA & NBB & (NNC & NOD | NOC & NND) | NBC & NBD & (NNA & NOB | NOA & NNB) | \
         (NBA & NOB | NOA & NBB ) & (NNC & NBD | NOC & NOD | NBC & NND) | \
         (NBC & NOD | NOC & NBD ) & (NNA & NBB | NOA & NOB | NBA & NNB)

    P4 = ~(P0 | P1 | P2 | P3 | P5 | P6 | P7 | P8)
    N4 = ~(N0 | N1 | N2 | N3 | N5 | N6 | N7 | N8)

    SG = (P6 & N0) | (P7 & N1)
    SF = (N6 & P0) | (N7 & P1)

    SE = P5 & (N1 | N0) | P6 & (N2 | N1) | P4 & N0
    SD = N5 & (P1 | P0) | N6 & (P2 | P1) | N4 & P0

    SC = P8 | N0 & (P3 | P7) | (P4 & N1) | (P5 & N2)
    SB = N8 | P0 & (N3 | N7) | (N4 & P1) | (N5 & P2)

    SA = N0 & (P0 | P1 | P2) | N4 & (P4 | P3 | P2) |\
        N1 & (P0 | P1 | P3 | P2) | N2 & (P0 | P1 | P4 | P3 | P2) |\
        N3 & (P1 | P5 | P4 | P3 | P2) |\
        P3 & N5

    Z1 = ~SA & (SB | ~(Y0 | Y1) & SD | (Y0 | Y1) & SG | Y1 & (SD | SE))
    Z0 = ~SA & (SC | ~(Y0 | Y1) & SE | (Y0 | Y1) & SF | Y0 & (SD | SE))
 
    return Z0, Z1
 
def out(x, y):
    out = ""
    for i in range(H):
        for j in range(W):
            a = (x >> (j + W * i)) & 1
            b = (y >> (j + W * i)) & 1

            if a:
                out += "#"
            elif b:
                out += "."
            else:
                out += " "
        out += "\n"
 
    print(out)
 
data_p = random.randint(0, 2**B)
data_n = random.randint(0, 2**B)

data_p &= random.randint(0, 2**B)
data_n &= random.randint(0, 2**B)

data_n &= ~data_p


while True:
    out(data_p, data_n)
    data_p, data_n = transform(data_p, data_n)
    sleep(0.05)
