#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import requests

resp = requests.get('http://localhost/ror/close')
if resp.ok:
    try:
        # requests.put('http://localhost/ror/close', timeout=0.001)
        resp = requests.put('http://localhost/ror/close')
    except:
        pass
sys.exit(0 if resp.ok else 1)