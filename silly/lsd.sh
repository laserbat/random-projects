#!/bin/bash
x=1 y=1 z=1 o=$(xrandr|grep primary|cut -d' ' -f1)
f(){ bc<<<"scale=5;x=$1;y=($RANDOM/32767-0.5)/10;if(x+y>0.5&&x+y<1.5)x+=y;print x;";}
trap "xrandr --output \"$o\" --gamma '1:1:1'" EXIT
while true; do
    x=$(f $x) y=$(f $y) z=$(f $z)
    xrandr --output "$o" --gamma "$x:$y:$z"
    sleep 0.1
done
