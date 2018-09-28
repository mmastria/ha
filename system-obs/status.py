#!/usr/bin/python

import sys
import ror 

script, path = sys.argv

status = open(path, 'w')
status.truncate()
status.write(ror.status())
status.close()
sys.exit(0)

