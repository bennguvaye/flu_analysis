#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import re

doss = sys.argv[1]
flush_number = sys.argv[2]

for fname in os.listdir(doss) :
  keep_lines = list()
  with open(doss + "/" + fname, 'rb') as fich :
    for i, line in enumerate(fich) :
      if i >= flush_number :
        keep_lines.append(line)

  with open(doss + "/" + fname, 'wb') as fich :
    for line in keep_lines :
      fich.write(line)
