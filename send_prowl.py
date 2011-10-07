#! /usr/bin/env python2.6

import prowlpy
import sys
from my_password import (p_prowl)
import syslog

# specify our log file, here local0 !
syslog.openlog('prowl', 0, syslog.LOG_LOCAL0)

p = prowlpy.Prowl(p_prowl.key)
try:
    p.add('Deluge','Finished download',sys.argv[1], 0, None, None)
except Exception,msg:
    syslog.syslog(syslog.LOG_ERR,'prowl error' + sys.argv[1])
	
