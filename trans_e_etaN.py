#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import math
import re

def x_transfo(x) :
  return x

def y_transfo(y) :
 return 10 ** y

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
