#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import re

doss = sys.argv[1]

for fname in os.listdir(doss) :
  with open(doss + "/" + fname, 'rb') as fich :
    sys.stdout.write(fich.read())
    
