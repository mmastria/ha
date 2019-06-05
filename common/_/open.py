#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import requests

resp = requests.get('http://localhost/ror/open')
if resp.ok:
    try:
        # requests.put('http://localhost/open', timeout=0.001)
        resp = requests.put('http://localhost/ror/open')
    except:
      pass
sys.exit(0 if resp.ok else 1)
