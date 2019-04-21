#!/bin/bash
sed -En "
/array2d/!d
s/.*\[(0.*)\].*/\1/
s/[, ]//g
s/-1/A/g
s/1/B/g
s/0/./g
s/(.{$1})/\1$\n/g
s/^/x = $1, y = $1, rule = BTCA1\n/p"
