#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import requests

resp = requests.put('http://localhost/ror/unpark')
sys.exit(0 if resp.ok else 1)

