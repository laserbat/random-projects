#!/bin/bash
while true; do
    minisat -verb=0 ./gol_grid.cnf ./solution
    ./show.py < ./solution
    ./neg.py < ./solution >> ./gol_grid.cnf
done
