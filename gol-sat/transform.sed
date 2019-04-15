#!/bin/sed -Ef
s/\), / 0\n/g
s/$/ 0/
s/(Or|And)\(//g
s/\)\)//g
s/,//g
s/~/-/g
y/abcdiefgh/ABCDEFGHI/
