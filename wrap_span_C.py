#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import argparse
import sys

parser = argparse.ArgumentParser(description=
  "Wrapper for span_pars that assumes that the matrix is square, and that\n"
  +"the transformation file is trans_str(x)_str(y) and that stuff goes in the\n"
  +"usual places.")

parser.add_argument("--fit",
                    choices=["empi", "theo", "idf", "isra"],
                    default="empi",
                    help="the set of parameter values that should be used")

parser.add_argument("--res",
                    default="10",
                    help="number of values per side.")

parser.add_argument("--start_ind",
                    default=0,
                    help="Starting global index for the set of simulations.")

parser.add_argument("x")
parser.add_argument("xmin")
parser.add_argument("xmax")

args = vars(parser.parse_args())

if args['fit'] == "empi" :
  args['par_string'] = ""
elif args['fit'] == "theo" :
  args['par_string'] = \
    "-R0 5. -nu 0.125 -g 0.000196"
elif args['fit'] == "idf" :
  args['par_string'] = \
    "-R0 1.96 -nu 0.336 -g 0.000457"
else :
  args['par_string'] = \
    "-R0 1.6 -nu 0.336 -g 0.000457"

args['npoints'] = str(int(args['res']))
# do a Rscript before to change par values. Would that work ?
sys.stdout.write(
"""python3 span_pars.py --prefix "/usr/bin/Rscript /import/ec_ecologie/bnguyen/flu/C/data/params.r {par_string} glob_ind" -x {x} {res} {xmin} {xmax} --transfo trans_C --suffix '''
./pandemics.native {start_ind} glob_ind''' --header '''#!/usr/bin/zsh
cd /import/ec_ecologie/bnguyen/flu/C/src
/bin/mkdir {start_ind} glob_ind''' --nfiles {npoints} --root_path ../scripts/C_{x}_{npoints} --save_pars_mat ../../data/C_{x}_{npoints}_pars.csv\n""".format(**args))

