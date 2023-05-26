#!/bin/bash
bsz=$1;
N=$2;
for nf in "${@:3}"; do
    echo "Launch ClDL for $nf (bsz=$bsz,#=$n) [3 thr.]";
    for typ in tw opt phs mytw myphs myphs0 myopt myopt0; do
       ./cldl.sage $nf $typ $bsz $N  2>&1 1> ../logs/$nf_${typ}.cldllog_${bsz}_${N} & 
    done;
done;
exit 0;
