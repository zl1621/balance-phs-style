

# This file was *autogenerated* from the file ./eval_geo.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_13 = Integer(13); _sage_const_14 = Integer(14); _sage_const_16 = Integer(16); _sage_const_5 = Integer(5); _sage_const_4 = Integer(4); _sage_const_6 = Integer(6); _sage_const_10 = Integer(10); _sage_const_500 = Integer(500); _sage_const_100 = Integer(100); _sage_const_180 = Integer(180)#!/usr/bin/env sage

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
print ("{}: eval geometry of log S-unit lattices".format(tag), flush=True);
if (tag[_sage_const_0 ] == 'z'):
    textag = "\\cyclo{" + tag[_sage_const_1 :] + "}";
elif (tag[_sage_const_0 ] == 'n'):
    textag = "\\ntru{"  + tag[_sage_const_1 :] + "}";
else:
    textag = tag;


# --------------------------------------------------------------------------------------
# Lattice file names: <data_dir>/<tag>/<tag>_<typ>.lat / <data_dir>/<tag>/<tag>_<typ>.bkz
data_dir = "./data/"+tag+"/";
typ_list = ["tw", "opt0", "phs0", "opt", "phs","mytw","myphs","myphs0","myopt","myopt0"]; # typ0 versions correspond to algo typ using twFB
textyp   = {"tw": "\\tw   ", "opt0": "\\opttwfb", "phs0": "\\phstwfb", "opt": "\\opt  ", "phs": "\\phs  ","mytw": "\\mytw   ",  "myphs": "\\myphs   ", "myphs0": "\\myphs0   ", "myopt": "\\myopt ","myopt0": "\\myopt0   "};

file_out = data_dir + tag + ".geo";
tex_out  = data_dir + tag + ".geo.tab";


# --------------------------------------------------------------------------------------
# Headings
f_out = open(file_out, "w");
f_out.write("# nf:'{}' Lines: {}=1 {}=2 {}=3 {}=4 {}=5 {}=6 {}=7 {}=8 {}=9 {}=10 \n".format(tag, *typ_list));
f_out.write("# dim\trvol\ther.\therbkz\todef\todefbkz\tthmin\tthmibkz\tthmoy\tthmobkz\tcov2\tcovinf\t[H.rat.\tH.exp.:only for tw]\n");
f_out.flush();

def print_data_line(f_out, typ, data):
    f_out.write(("{}"+"\t{:7.3f}"*_sage_const_13 +"\t//[{}]\n").format(*([data[_sage_const_0 ]]+[float(_d) for _d in data[_sage_const_1 :_sage_const_14 ]]+[typ])));
    f_out.flush();

tex_out = open(tex_out, "w");
tex_out.write("%% nf:'{}' Lines: {}=1 {}=2 {}=3 {}=4 {}=5 {}=6 {}=7 ={}8 ={}9 ={}10 \n".format(tag, *typ_list));
tex_out.write("%% typ\t\tdim\tredvol\therm\thermbkz\todef\todefbkz\tthmin\tthmibkz\tthmoy\tthmobkz\tcov2\tcovinf\tratreal\tratheur\n");
tex_out.write("\\multirow{8}{*}{$\\QQ("+textag+")$}%\n");
tex_out.flush();


def print_texdata_line(tex_out, typ, data):
    RRout = RealField(_sage_const_16 );
    tex_out.write(("& {}"+"\t& {}"+"\t& {}"*_sage_const_5 +"\t& {}"*_sage_const_4 +"\t& {}"*_sage_const_4 +"\t\\\\* %[{}]\n").format(textyp.get(typ), *([data[_sage_const_0 ]] + [str(RRout(_d))[:_sage_const_5 ] for _d in data[_sage_const_1 :_sage_const_6 ]] + [round(_d) for _d in data[_sage_const_6 :_sage_const_10 ]] + [ str(RRout(_d))[:_sage_const_5 ] for _d in data[_sage_const_10 :_sage_const_14 ]]), typ));
    tex_out.flush();


# Eval covering radii, using Babai NP on the BKZ reduced matrix
from sage.stats.distributions.discrete_gaussian_integer import DiscreteGaussianDistributionIntegerSampler
NTESTS=_sage_const_500 ;
def eval_covering_radii(K, B, do_rat):
    n   = K.degree();
    r1, r2 = K.signature();
    urk = get_rank_units(K);
    k   = B.nrows()-urk;
    w_prec = B.base_ring().precision();
    
    #t = cputime();
    D = DiscreteGaussianDistributionIntegerSampler(sigma=_sage_const_100 *B.nrows()*_sage_const_2 **w_prec);
    #t = cputime(t); print (" Gaussian time={:.2f}", t);

    # Precompute G-S ortho of B
    _GSB, _ = gram_schmidt_ortho(B, normalize=False);
    # If algo is TW, compute fH
    invfH = _sage_const_0 ;
    if (do_rat == True):
        invfH = get_twfHcE_matrix(r1, r2, [_sage_const_0 ]*k, 'TW', b_prec=w_prec).transpose();

    mu_2   = _sage_const_0 ;
    mu_inf = _sage_const_0 ;
    fH_rat = _sage_const_0 ;
    exp_rat = RealField(w_prec)(ln(n+k)/sqrt(n+k)) if (do_rat == True) else RealField(w_prec)(ln(urk+k)/sqrt(urk+k));
    for i in range(NTESTS):
        t  = vector(RealField(w_prec), [D()/_sage_const_2 **w_prec for i in range(B.nrows())]);
        v  = cvp_babai_NP(B, t, G=_GSB);
        v_d  = (v-t);
        l2   = v_d.norm(_sage_const_2 );
        linf = v_d.norm(infinity);
        # Covering adjustments
        mu_2   = max(mu_2, l2);
        mu_inf = max(mu_inf, linf);
        # If tw, evaluate H3.8
        if (do_rat == True):
            v_d_rat = (v_d*invfH).norm(infinity) / l2 / exp_rat;
        else:
            v_d_rat = linf / l2 / exp_rat;
        fH_rat  = fH_rat + v_d_rat;
            
    fH_rat = fH_rat / RealField(w_prec)(NTESTS);
    return mu_2, mu_inf, fH_rat, exp_rat;
    

    
for i in range(len(typ_list)):
    typ = typ_list[i];
    print ("'{}' method".format(typ), flush=True);

    # Reading lattices
    L_file = data_dir + tag + "_" + typ + ".lat";
    B_file = data_dir + tag + "_" + typ + ".bkz";
    if (not os.path.exists(L_file)):
        print ("    [next] Log S-unit lat file '{}' does not exist.".format(L_file), flush=True);
        f_out.write("0\t//[{}]\n".format(typ));
        continue;
    if (not os.path.exists(B_file)):
        print ("    [next] Bkz file '{}' does not exist.".format(B_file), flush=True);
        f_out.write("0\t//[{}]\n".format(typ));
        continue;
    print("    Reading data...", flush=True, end='');
    L = lattice_read_data(L_file);
    B = lattice_read_data(B_file);
    Lw = L.change_ring(B.base_ring());
    print("\t[done]", flush=True);
    
    # Dimension
    _dim = B.nrows();
    
    # Reduced volume
    print("    Reduced volume", flush=True);
    _r_vol = vol_reduced(L);
    assert(fp.fp_check_zero("vol(L)=vol(BKZ)", [_r_vol - vol_reduced(B)], target=B.base_ring().precision(), sloppy=True));
    
    # Hermite before/after BKZ
    print("    Root Hermite factors", flush=True);
    _d0     = rankin_reduced(Lw, _sage_const_1 );
    _d0_bkz = rankin_reduced(B, _sage_const_1 );
        
    # Ortho defect before/after BKZ
    print("    Orthogonality defect", flush=True);
    _dn     = rankin_reduced(Lw, L.nrows());
    _dn_bkz = rankin_reduced(B, B.nrows());
        
    # Th.min before/after BKZ
    print("    Min angle", flush=True);
    _th_min     = min_angle(Lw);
    _th_min_bkz = min_angle(B);
    # Th.moy before/after BKZ
    print("    Mean_angle", flush=True);
    _th_moy     = mean_angle(Lw);
    _th_moy_bkz = mean_angle(B);

    # cov2/covinf/twisted (opt)
    print("    Eval cov radius...", flush=True, end='');
    t = cputime();
    _cov2, _cov_inf, _fHrat, _exp = eval_covering_radii(K, B, (typ=="tw"));
    t = cputime(t);
    print("\t[done] t={:.2f}".format(t), flush=True);
    
    # Output
    data_line = [_dim, _r_vol, _d0, _d0_bkz, _dn, _dn_bkz, _th_min*_sage_const_180 /pi, _th_min_bkz*_sage_const_180 /pi,
                 _th_moy*_sage_const_180 /pi, _th_moy_bkz*_sage_const_180 /pi, _cov2, _cov_inf, _fHrat, _exp ];
    print_data_line(f_out, typ, data_line);
    print_texdata_line(tex_out, typ, data_line);

tex_out.write("\\hline\n");    
tex_out.close();
f_out.close();
exit;


