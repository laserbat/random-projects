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
    PQA, PRA, PSA = variables(x, 1)
    PQB, PRB, PSB = variables(x, W - 1)
    PQC, PRC, PSC = variables(x, W)
    PQD, PRD, PSD = variables(x, W + 1)

    NQA, NRA, NSA = variables(y, 1)
    NQB, NRB, NSB = variables(y, W - 1)
    NQC, NRC, NSC = variables(y, W)
    NQD, NRD, NSD = variables(y, W + 1)

    Y0 = x
    Y1 = y

    P0 = PRA & PRB & PRC & PRD
    N0 = NRA & NRB & NRC & NRD

    P8 = PQA & PQB & PQC & PQD
    N8 = NQA & NQB & NQC & NQD

    P1 = PRA & PRB & (PRC & PSD | PRD & PSC) | PRC & PRD & (PRA & PSB | PSA & PRB)
    N1 = NRA & NRB & (NRC & NSD | NRD & NSC) | NRC & NRD & (NRA & NSB | NSA & NRB)

    P7 = PQA & PQB & (PQC & PSD | PQD & PSC) | PQC & PQD & (PQA & PSB | PSA & PQB)
    N7 = NQA & NQB & (NQC & NSD | NQD & NSC) | NQC & NQD & (NQA & NSB | NSA & NQB)

    P2 = PRA & PRB & (PQC & PRD | PSC & PSD | PRC & PQD) |  PRC & PRD & (PQA & PRB | PSA & PSB | PRA & PQB) |\
        ((PRA & PSB) | (PSA & PRB)) & ((PRC & PSD) | (PSC & PRD))

    N2 = NRA & NRB & (NQC & NRD | NSC & NSD | NRC & NQD) |  NRC & NRD & (NQA & NRB | NSA & NSB | NRA & NQB) |\
        ((NRA & NSB) | (NSA & NRB)) & ((NRC & NSD) | (NSC & NRD))

    P6 = PQA & PQB & (PRC & PQD | PSC & PSD | PQC & PRD) |  PQC & PQD & (PRA & PQB | PSA & PSB | PQA & PRB) |\
        ((PQA & PSB) | (PSA & PQB)) & ((PQC & PSD) | (PSC & PQD))

    N6 = NQA & NQB & (NRC & NQD | NSC & NSD | NQC & NRD) |  NQC & NQD & (NRA & NQB | NSA & NSB | NQA & NRB) |\
        ((NQA & NSB) | (NSA & NQB)) & ((NQC & NSD) | (NSC & NQD))

    P3 = PRA & PRB & (PQC & PSD | PSC & PQD) | PRC & PRD & (PQA & PSB | PSA & PQB) | \
         (PRA & PSB | PSA & PRB ) & (PQC & PRD | PSC & PSD | PRC & PQD) |  \
         (PRC & PSD | PSC & PRD ) & (PQA & PRB | PSA & PSB | PRA & PQB)

    N3 = NRA & NRB & (NQC & NSD | NSC & NQD) | NRC & NRD & (NQA & NSB | NSA & NQB) | \
         (NRA & NSB | NSA & NRB ) & (NQC & NRD | NSC & NSD | NRC & NQD) | \
         (NRC & NSD | NSC & NRD ) & (NQA & NRB | NSA & NSB | NRA & NQB)


    P5 = PQA & PQB & (PRC & PSD | PSC & PRD) | PQC & PQD & (PRA & PSB | PSA & PRB) | \
         (PQA & PSB | PSA & PQB ) & (PRC & PQD | PSC & PSD | PQC & PRD) | \
         (PQC & PSD | PSC & PQD ) & (PRA & PQB | PSA & PSB | PQA & PRB)

    N5 = NQA & NQB & (NRC & NSD | NSC & NRD) | NQC & NQD & (NRA & NSB | NSA & NRB) | \
         (NQA & NSB | NSA & NQB ) & (NRC & NQD | NSC & NSD | NQC & NRD) | \
         (NQC & NSD | NSC & NQD ) & (NRA & NQB | NSA & NSB | NQA & NRB)

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
