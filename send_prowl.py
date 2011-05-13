#! /usr/bin/env python2.6

import prowlpy
import sys
from my_password import (p_prowl)

p = prowlpy.Prowl(p_prowl.key)
try:
    p.add('Transmission','Finished download',sys.argv[1], 0, None, None)
except Exception,msg:
    print msg
