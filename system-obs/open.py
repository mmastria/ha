#!/usr/bin/python
#
# Open shutter script for INDI Dome Scripting Gateway
#
# Arguments: none
# Exit code: 0 for success, 1 for failure
#

import sys

coordinates = open('/tmp/indi-status', 'r')
str = coordinates.readline()
coordinates.close()
str = str[0] + ' 1 ' + str[4:]
coordinates = open('/tmp/indi-status', 'w')
coordinates.truncate()
coordinates.write(str)
coordinates.close()

sys.exit(0)

