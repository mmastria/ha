#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import requests

#script, path = sys.argv
script = sys.argv

resp = requests.get('http://localhost/ror/status')
if resp.ok:
    #status = open(path, 'w')
    status = open('/tmp/indi-status', 'w')
    status.truncate()
    status.write(resp.content)
    status.close()
    sys.exit(0)
sys.exit(1)

