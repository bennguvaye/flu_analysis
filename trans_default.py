#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import math
import re

def id_transfo(x) :
  return x

def etaN_transfo(y) :
 return 10 ** y

def g_transfo(y) :
  return 1. / (y * 365)


vars_transfo = {'e':id_transfo, 'R0':id_transfo,
                'etaN':etaN_transfo, 'etaN1':etaN_transfo, 
                'etaN2':etaN_transfo, 'sceta':etaN_transfo,
                'g':g_transfo, 'g1':g_transfo, 'g2':g_transfo}

# create the right file
def header_transfo(s, i) :
  return re.sub(r'''touch (\S*)''',
                '''touch \\1/''' + str(i),
                s)

def prefix_transfo(s, i, j) :
  return s

# append to the right file, after adding "i, j, " at the beginning of the line
def suffix_transfo(s, i, j) :
  return re.sub(r'''>> (\S*)''', 
                '''| awk \'{print \"''' + str(i) + ''', ''' + str(j) + ''', \"$0}\' >>  \\1/''' + str(i),
                s)
