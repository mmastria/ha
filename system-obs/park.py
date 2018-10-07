#!/usr/bin/python

import sys
import requests

resp = requests.put('http://localhost/park')
exit(0 if resp.ok else 1)
  
