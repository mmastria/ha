#!/bin/bash
ls -1 /home/west/.indi/*_config.xml|xargs -r -n 1 -I{} cp {} {}.default
ls -1 /home/west/.indi/*_config.xml.default|xargs -r -n 1 -I{} cp {} .