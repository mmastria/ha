#!/usr/bin/python

import sys
import requests

resp = requests.get('http://localhost/close')
if resp.ok:
  try:
    #requests.put('http://localhost/close', timeout=0.001)
    resp = requests.put('http://localhost/close')
  except:
    pass
exit(0 if resp.ok else 1)
  
