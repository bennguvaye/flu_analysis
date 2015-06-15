#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

import math
import re

def x_transfo(x) :
  return 10 ** x

def y_transfo(y) :
  return 1. / (y * 365)

def prefix_transfo(s, i, j) :
  return s

def suffix_transfo(s, i, j) :
  return re.sub(r'''>> (\S*)''', 
                '''| awk \'{print \"''' + str(j) + '''\"$0}\' >>  \\1_''' + str(i),
                s)
