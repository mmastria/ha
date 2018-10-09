#!/usr/bin/python

import sys
import requests

resp = requests.get('http://localhost/park')
if resp.ok:
  try:
    #requests.put('http://localhost/park', timeout=0.001)
    resp = requests.put('http://localhost/park')
  except:
    pass
exit(0 if resp.ok else 1)
  
