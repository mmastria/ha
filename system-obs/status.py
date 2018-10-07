#!/usr/bin/python

import sys
import requests
#import json

script, path = sys.argv

resp = requests.get('http://localhost/status')
if resp.ok:
  status = open(path, 'w')
  status.truncate()
  status.write(resp.content)
  status.close()
  sys.exit(0)
sys.exit(1)

