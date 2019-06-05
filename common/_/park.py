#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import requests

resp = requests.get('http://localhost/ror/park')
if resp.ok:
    try:
        # requests.put('http://localhost/ror/park', timeout=0.001)
        resp = requests.put('http://localhost/ror/park')
    except:
        pass
sys.exit(0 if resp.ok else 1)