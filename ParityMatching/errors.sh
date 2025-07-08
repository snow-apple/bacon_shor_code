#!/bin/bash

ds=3
de=4
dd=2
ps=0.2
pe=0.3
dp=0.1
bp=0
ns=1
x=36

for ((i=0; i<x; i++)); do
    ./baconshor "$ds" "$de" "$dd" "$ps" "$pe" "$dp" "$bp" "$ns" "$i"
done
