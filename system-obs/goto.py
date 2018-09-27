#!/usr/bin/python
#
# Goto azimuth script for INDI Dome Scripting Gateway
#
# Arguments: Az
# Exit code: 0 for success, 1 for failure
#

import sys

script, az = sys.argv

coordinates = open('/tmp/indi-status', 'r')
str = coordinates.readline()
coordinates.close()
str = str[0:3] + az
coordinates = open('/tmp/indi-status', 'w')
coordinates.truncate()
coordinates.write(str)
coordinates.close()

sys.exit(0)

