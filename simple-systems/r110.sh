#!/bin/sh
# unixy way to simulate rule 110
W=200; perl -e "print'0 1'.'0'x$W" | sed -E ':a;s/(^(0) 1(11)| 0(1)| (.))(.*)/\2 \3\4\6\5\4\2/p;ba' | awk "NR%$W==0" | tr '01' '.#' | less
