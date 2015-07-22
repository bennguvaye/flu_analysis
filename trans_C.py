#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import math
import re

def e_transfo(x) :
  return x

def etaN_transfo(y) :
 return 10 ** y

def g_transfo(y) :
  return 1. / (y * 365)


vars_transfo = {'e':e_transfo, 
                'etaN':etaN_transfo, 'etaN1':etaN_transfo, 'etaN2':etaN_transfo,
                'g':g_transfo, 'g1':g_transfo, 'g2':g_transfo}

# create the right file
def header_transfo(s, i) :
  return re.sub(r'''[0-9]+ glob_ind''',
                str(i),
                s)

def prefix_transfo(s, i, j) :
  return re.sub(r'''glob_ind''',
                str(i),
                s)

# append to the right file, after adding "i, j, " at the beginning of the line
def suffix_transfo(s, i, j) :
  return re.sub(r'''[0-9]+ glob_ind''', 
                str(i),
                s)
