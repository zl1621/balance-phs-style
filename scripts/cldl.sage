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

if len(sys.argv) !=5:
    print("Usage: {:s} <nf_tag>, nf_tag is :\n\tz<m> for Cyclotomic of conductor m\n\tn<p> for NTRU Prime fields of degree p\n".format(sys.argv[0]));
    sys.exit(2);

tag=sys.argv[1];
typ=sys.argv[2];
bsz=sys.argv[3];
nb=sys.argv[4];


K=nf_set_tag(tag);

data_dir = "./data/"+tag+"/";
fb_file= data_dir+tag+"_"+typ+".fb";
_fb_file=open(fb_file,"r");
next(_fb_file);
FB=fb_in_stream(_fb_file,K);
#chal_file=data_dir+tag+"."+chal+"_b"+bsz+"_n"+nb;
chal_file="{}.chal_b{}_n{}".format(data_dir+tag,bsz,nb);
_c_chal_file=open(chal_file,"r");
next(_c_chal_file);
cc=chal_in_stream(_c_chal_file,K);
#out_file=data_dir+tag+"_"+typ+.cldl+_b+bsz+_n+len(cc);
out_file="{}_{}.cldl_b{}_n{}".format(data_dir+tag,typ,bsz,len(cc));

print("{} clDL for typ={}, in={}\n".format(tag,typ,chal_file));

out=open(out_file,"w");
nf_out_stream(out,K);
out.write("# cldl({}): typ={} bsz={} k={}\n".format(chal_file,typ,bsz,len(cc)));


for k in range(len(cc)):
    _cc=cc[k];
    print("Challenge #{}...".format(k));
    t=cputime();
    eta= get_id_clDL(K,_cc,FB,[]); 
    t=cputime(t);
    print("\t[done] t={}\n".format(t));
    #__su_out_stream(out,K,eta);
    out.write("{}\n".format(str(eta.polynomial().list()).replace(' ', '')));
    
out.write("#--- END --- \n");
out.close();

exit;


