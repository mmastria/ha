#!/usr/bin/python

import sys
#import ror

script, path = sys.argv

#status = open(path, 'w')
#status.truncate()
#status.write(ror.status())
#status.close()
st = open('/tmp/ror-status', 'w')
st.truncate()
st.write(path)
st.close()
sys.exit(0)

