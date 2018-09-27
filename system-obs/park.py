#!/usr/bin/python
#
# Park script for INDI Dome Scripting Gateway
#
# Arguments: none
# Exit code: 0 for success, 1 for failure
#

import sys

coordinates = open('/tmp/indi-status', 'w')
coordinates.truncate()
coordinates.write('1 0 0')
coordinates.close()

sys.exit(0)

