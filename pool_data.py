#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import re

doss = sys.argv[1]

for fname in os.listdir(doss) :
  ij = re.sub(r"etag_90000_([0-9]+)_([0-9]+)",
              r"\1, \2, ",
              fname)
  with open(doss + "/" + fname, 'rb') as fich :
    data = fich.read()
    to_be_written = ij + data
    sys.stdout.write(to_be_written)
    
