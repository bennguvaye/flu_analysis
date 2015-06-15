#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import argparse
import importlib
import csv

parser = argparse.ArgumentParser(description=
  "Store in nfiles commands to run prog on arguments spanning xmin -> xmax and ymin -> ymax")

parser.add_argument("--prefix",
                    type=str,
                    required=True,
                    help="string to put before the arguments. Typically the executable")
parser.add_argument("--suffix",
                    type=str,
                    default="",
                    help="string to put after the arguments. Typically other arguments, pipes, etc...")

parser.add_argument("-x",
                    nargs=4,
                    required=True,
                    help="expects the keyword, number of values,"
                        +" min value and max value for the first argument")

parser.add_argument("-y",
                    nargs=4,
                    required=False,
                    help="expects the keyword, number of values," 
                        +" min value and max value for the second argument")

parser.add_argument("--nfiles",
                    type=int,
                    default=1,
                    help="the number of files to generate")

parser.add_argument("--root_path",
                    type=str,
                    default="run_with_pars",
                    help="the root name of the files to generate")

parser.add_argument("--transfo",
                    type=str,
                    required=False,
                    default="transfo_default",
                    help="a python module containing functions x_transfo" + 
                    " (and y_transfo) for transformation to apply to x" +
                    " and y before using them in the program")

parser.add_argument("--save_pars_mat",
                    type=str,
                    default="/dev/null",
                    help="where to save the matrix of parameter values." + 
                         "Default : doesn't save.")

pars = parser.parse_args()

prefix = pars.prefix
suffix = pars.suffix

x_key = pars.x[0]
nx = int(pars.x[1])
xmin = float(pars.x[2])
xmax = float(pars.x[3])

one_param = False
try :
  y_key = pars.y[0]
  ny = int(pars.y[1])
  ymin = float(pars.y[2])
  ymax = float(pars.y[3])
except TypeError :
  one_param = True
  
nfiles = pars.nfiles
root_path = pars.root_path

tr = importlib.import_module(pars.transfo)

def output_info(n1, n2) :
  print("Each file contains " 
        + str(n1) + " values.")
  print("Except the last one, which contains " 
        + str(n2) + " values.")

if one_param :
  x_step = (xmax - xmin) / nx
  n_vals_per_files = nx // nfiles
  n_vals_per_last_file = n_vals_per_files + nx % nfiles
  output_info(n_vals_per_files, n_vals_per_last_file)

  pars_l = list()
  pars_l.append(["i", "j", x_key])

  def next_val(x) :
    if x + x_step > xmax : 
      raise ValueError
    else :
      return x + x_step

  def one_str(x, i, j) :
    mastr =  tr.prefix_transfo(prefix, i, j) \
      + " -" + x_key + " " + str(tr.x_transfo(x)) \
      + tr.suffix_transfo(suffix, i, j) \
      + "\n"
    return mastr

  x = xmin
  
  for i in range(nfiles - 1) :
    with open(root_path + "_" + str(i), 'w') as fich :
      fich.write("#!/usr/bin/zsh\n")
      for j in range(n_vals_per_files) :
        fich.write(one_str(x, i, j))
        pars_l.append([str(i), str(j), str(x)])
        x = next_val(x)
  
  with open(root_path + "_" + str(nfiles - 1), 'w') as fich :
    fich.write("#!/usr/bin/zsh\n")
    for j in range(n_vals_per_last_file) :
        fich.write(one_str(x, nfiles - 1, j))
        try :
          x = next_val(x)
        except ValueError :
          break

else : # we iterate over two parameters
  x_step = (xmax - xmin) / nx
  y_step = (ymax - ymin) / ny
  
  n_vals_per_files = nx * ny // nfiles
  n_vals_per_last_file = n_vals_per_files + (nx * ny) % nfiles
  output_info(n_vals_per_files, n_vals_per_last_file)

  pars_l = list()
  pars_l.append(["i", "j", x_key, y_key])
  
  def two_str(x, y, i, j) :
    mastr = tr.prefix_transfo(prefix, i, j) \
      + " -" + x_key + " " + str(tr.x_transfo(x)) \
      + " -" + y_key + " " + str(tr.y_transfo(y)) \
      + tr.suffix_transfo(suffix, i, j) \
      + "\n" 
    return mastr

  def next_val(x, y) :
    if y + y_step < ymax :
      return (x, y + y_step)
    else :
      if x + x_step <= xmax :
        return (x + x_step, ymin)
      else :
        raise ValueError
        
  x = xmin
  y = ymin
  
  for i in range(nfiles - 1) :
    with open(root_path + "_" + str(i), 'w') as fich :
      fich.write("#!/usr/bin/zsh\n")
      for j in range(n_vals_per_files) :
        fich.write(two_str(x, y, i, j)) 
        pars_l.append([str(i), str(j), str(x), str(y)])
        x, y = next_val(x, y)
                
  
  with open(root_path + "_" + str(nfiles - 1), 'w') as fich :
    fich.write("#!/usr/bin/zsh\n")
    for j in range(n_vals_per_last_file) :
        fich.write(two_str(x, y, nfiles - 1, j))
        pars_l.append([str(i), str(j), str(x), str(y)])
        try :
          x, y = next_val(x, y)
        except ValueError :
          break

with open(pars.save_pars_mat, 'w', newline='') as csvfile :
  wri = csv.writer(csvfile, delimiter=',')
  wri.writerows(pars_l)
