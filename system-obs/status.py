#!/usr/bin/python
#
# Status script for INDI Dome Scripting Gateway
#
# Arguments: file name to save current state and coordinates (parked ra dec)
# Exit code: 0 for success, 1 for failure
#

import sys

script, path = sys.argv

coordinates = open('/tmp/indi-status', 'r')
status = open(path, 'w')
status.truncate()
status.write(coordinates.readline())
status.close()

sys.exit(0)

