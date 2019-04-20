#!/bin/perl

# It is possible to do a Turing-complete computation by applying a single simple regex
# (no backrefs or any black magic) in a loop.

# Proof is done by simulation of rule110

# World should start with '0 ' and end with 'q'
$world = "0 1q";
 
while(){
    $world =~ s/(^(0) (q)|^(0) 1(11)| 0(1)| (.))(.*)/\2\4 \5\6\8\7\6\4\3\2/;
 
    # This is simply output code
    # It's not necessary for the computation
    if ($world =~ /^0 q/) {
        $_ = $world;
        s/....//;
        y/01.#/.#01/;
        print "$_\n";
    }
}
