#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import argparse
import sys

parser = argparse.ArgumentParser(description=
  "Wrapper for span_pars that assumes that the matrix is square, and that\n"
  +"the transformation file is trans_str(x)_str(y) and that stuff goes in the\n"
  +"usual places.")

parser.add_argument("--exe", 
                    choices=["ssd", "dsd", "sss", "dss", "assd"],
                    default="ssd",
                    help="the identifier of the executable.")

parser.add_argument("--res",
                    default="100",
                    help="number of values per side.")

parser.add_argument("--nfiles",
                    default="100",
                    help="number of files to create.")

parser.add_argument("x")
parser.add_argument("xmin")
parser.add_argument("xmax")
parser.add_argument("y",
                    nargs="?",
                    default=None)
parser.add_argument("ymin",
                    nargs="?",
                    default=None)
parser.add_argument("ymax",
                    nargs="?",
                    default=None)

args = vars(parser.parse_args())

if not (args['y'], args['ymin'], args['ymax']) == (None, None, None) \
   or (args['y'] is not None and args['ymin'] is not None and args['ymax'] is not None) :
  raise ValueError("All or none of y, ymin and ymax must be set !")

if (args['y'], args['ymin'], args['ymax']) == (None, None, None) :
  args['npoints'] = str(int(args['res']))
  sys.stdout.write(
"""python3 span_pars.py --prefix "/import/ec_ecologie/bnguyen/flu/ocaml/sim_{exe}.native -tf 73000" -x {x} {res} {xmin} {xmax} --transfo trans_default --suffix " | /usr/bin/python /import/ec_ecologie/bnguyen/flu/python/get_peaktimes_det.py >> /import/ec_ecologie/bnguyen/flu/data/{exe}_{x}_{npoints}" --header '''#!/usr/bin/zsh
/usr/bin/touch /import/ec_ecologie/bnguyen/flu/data/{exe}_{x}_{npoints}''' --nfiles {nfiles} --root_path ../scripts/{exe}_{x}_{npoints} --save_pars_mat ../../data/{exe}_{x}_{npoints}_pars.csv\n""".format(**args))

else :
  args['npoints'] = str(int(args['res']) ** 2)
  sys.stdout.write(
"""python3 span_pars.py --prefix "/import/ec_ecologie/bnguyen/flu/ocaml/sim_{exe}.native -tf 182500" -x {x} {res} {xmin} {xmax} -y {y} {res} {ymin} {ymax} --transfo trans_default --suffix " | /usr/bin/python /import/ec_ecologie/bnguyen/flu/python/get_lyaper.py >> /import/ec_ecologie/bnguyen/flu/data/{exe}_{x}{y}_{npoints}" --header '''#!/usr/bin/zsh
/usr/bin/touch /import/ec_ecologie/bnguyen/flu/data/{exe}_{x}{y}_{npoints}''' --nfiles {nfiles} --root_path ../scripts/{exe}_{x}{y}_{npoints} --save_pars_mat ../../data/{exe}_{x}{y}_{npoints}_pars.csv\n""".format(**args))


