#!/bin/bash

for nf in "$@"; do
    echo "Launching S-Units for $nf";
    ./sunits.sage $nf  2>&1 1> ../logs/$nf.sulog & done;

exit 0;
