#!/bin/bash
ls -1 /home/obs/.indi/*_config.xml|xargs -r -n 1 -I{} cp -v {} {}.default
ls -1 /home/obs/.indi/*_config.xml.default|xargs -r -n 1 -I{} cp -v {} .
