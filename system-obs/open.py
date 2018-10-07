#!/usr/bin/python

import sys
import requests

resp = requests.get('http://localhost/open')
if resp.ok:
  try:
    requests.put('http://localhost/open', timeout=0.001)
  except:
    pass
exit(0 if resp.ok else 1)
  
