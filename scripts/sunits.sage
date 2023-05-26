#!/usr/bin/env sage

# Small convenient hack to simulate as if we were always executing from '<trunk>/'
import os
import sys
os.chdir(os.path.dirname(__file__) + "/../");
sys.path.append("./src/");
# ---------------------------------------------------------
# -----------------------------
from sage.all import *
from lattice import *
from number_field import *
from twphs_algo import *

if len(sys.argv) != 2:
    print("Usage: {:s} <nf_tag>, nf_tag is :\n\tz<m> for Cyclotomic of conductor m\n\tn<p> for NTRU Prime fields of degree p\n".format(sys.argv[0]));
    sys.exit(2);

tag = sys.argv[1];
K=nf_set_tag(tag);

data_dir = "./data/"+tag+"/";

for typ in ["tw", "opt", "phs","mytw","myphs","myphs0","myopt","myopt0"]:
    print("{}: Sunits for typ_fb='{}'...\n".format(tag, typ));
    _fb=data_dir+tag+"_"+typ+".fb";

    out=data_dir+tag+"_"+typ+".su";
    fb=open(_fb,"r");
    next(fb);
    FB=fb_in_stream(fb, K);
    t=cputime();
    S=get_S_units(K, FB)[1];
    t=cputime(t);
    print("\t[done] t={} hk={}\n".format(t,K.class_number())); 
    print("--> output in '{}'\n".format(out));
    _out=open(out,"w");
    _out.write("# number_field: tag={} eq={}\n".format(nf_get_tag(K), str(K.defining_polynomial().list()).replace(' ', '')));
    sunits_out_stream(_out, K, S[0], S[1]);
    _out.write("#--- END ---\n");

_out.close();

exit;