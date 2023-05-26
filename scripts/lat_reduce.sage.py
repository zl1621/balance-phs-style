

# This file was *autogenerated* from the file ./lat_reduce.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_500 = Integer(500); _sage_const_300 = Integer(300); _sage_const_40 = Integer(40); _sage_const_60 = Integer(60)#!/usr/bin/env sage

# Small convenient hack to simulate as if we were always executing from '<trunk>/'
import os
import sys
os.chdir(os.path.dirname(__file__) + "/../");
sys.path.append("./src/");
# --------------------------------------------------------------------------------------

from sage.all import *
import fp
from lattice import *
from number_field import *
from twphs_algo import *

if len(sys.argv) != _sage_const_2 :
    print("Usage: {:s} <nf_tag>, nf_tag is :\n\tz<m> for Cyclotomic of conductor m\n\tn<p> for NTRU Prime fields of degree p\n".format(sys.argv[_sage_const_0 ]));
    sys.exit(_sage_const_2 );

tag = sys.argv[_sage_const_1 ];


# --------------------------------------------------------------------------------------
# Obtain number field
K = nf_set_tag(tag);
print ("{}: reduce log S-unit lattices".format(tag), flush=True);


# --------------------------------------------------------------------------------------
# Output file names
data_dir  = "./data/"+tag+"/";
list_lats = [ data_dir+tag+"_"+_s+".lat" for _s in ["phs","phs0","myphs","myphs0", "opt","opt0", "myopt","myopt0", "tw","mytw"]];
out_bkz   = [ data_dir+tag+"_"+_s+".bkz" for _s in ["phs","phs0","myphs","myphs0", "opt","opt0", "myopt","myopt0", "tw","mytw"]];


#data_dir  = "./data/"+tag+"/";
#list_lats = [ data_dir+tag+"_"+_s+".lat" for _s in ["mytw"]];
#out_bkz   = [ data_dir+tag+"_"+_s+".bkz" for _s in ["mytw"]];


# --------------------------------------------------------------------------------------
# This part is easy, we work at (very) high precision just in case
MAX_PREC = _sage_const_500 ; # Beyond 500, fplll performance drops drastically (?)
MIN_PREC = _sage_const_300 ; # It works fine everywhere.
VOL_SCALE = _sage_const_2 ;  # Work at 2 times the volume log in base 2
MAX_LOOPS = _sage_const_300 ;
BLOCK_SZ  = _sage_const_40 ;
HKZ_MAX   = _sage_const_60 ;

# --------------------------------------------------------------------------------------
# For each of 'PHS', 'OPT', 'TW', load FB + SU, compute twlat and output
for i in range(len(list_lats)):
    lat_file = list_lats[i];
    out_file = out_bkz[i];
    if (not os.path.exists(lat_file)):
        print ("[next] Lat file '{}' does not exist.".format(lat_file), flush=True);
        continue;
    print ("Lat '{}'".format(lat_file), flush=True);

    # Input lattice
    L = lattice_read_data(lat_file);
    print ("    dim={}".format(L.nrows()), flush=True);

    # Determine precision
    logv = lnvol(L)/ln(L.base_ring()(_sage_const_2 ));
    print ("    logvol={:.2f}".format(float(logv)));
    assert (logv < MAX_PREC); # Otherwise it will fail
    work_prec = ceil(logv*VOL_SCALE);
    work_prec = MIN_PREC if work_prec < MIN_PREC else MAX_PREC if work_prec > MAX_PREC else work_prec;

    # Determine block_size
    block_sz = L.nrows() if (L.nrows() <= HKZ_MAX) else BLOCK_SZ;

    # Launching BKZ
    print ("    bkz bk={} prec={} nloops={} ...".format(block_sz, work_prec, MAX_LOOPS), flush=True, end='');
    #t = cputime(subprocesses=True);
    t = walltime();
    B = bkz(L, work_prec=work_prec, block_size=block_sz, bkzmaxloops=MAX_LOOPS)[_sage_const_0 ];
    t = walltime(t);
    print ("\t[done] t={:.2f}".format(t), flush=True);
    fp.fp_check_zero("vol(L)=vol(BKZ(L))", [lnvol(B)-lnvol(L)], target=work_prec, sloppy=True);
    
    # Output
    lattice_out_data(out_file, B);
    print ("    out -> '{}'".format(out_file), flush=True);

exit;

