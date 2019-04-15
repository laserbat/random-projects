#!/bin/bash
./gen_cnf.py | ./transform.sed > ./template.cnf
./gen_grid.py < ./template.cnf > ./gol_grid.cnf
