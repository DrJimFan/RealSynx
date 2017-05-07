#!/usr/bin/env python3
"""
Copy .realsync to .realsync2 ... .realsync<n>
"""

import os
import sys

if len(sys.argv) < 2:
    print(sys.argv[0], '<file_of_host_name> or "clear"')
    sys.exit(1)

assert os.path.exists('.realsync')

def prompt(msg):
    ans = input(msg)
    if ans.lower() in ['n', 'q']:
        sys.exit(1)

if sys.argv[1] == 'clear':
    prompt('Do you want to clear all .realsync<n>? ".realsync" itself will be preserved: ')
    os.system("find . -regex './.realsync[0-9][0-9]*' -delete")
    sys.exit(0)

hosts = []
for l in open(sys.argv[1]):
    l = l.strip()
    if l:
        hosts.append(l)
        print(l)
print('Creating', len(hosts), 'replicas.')
prompt('Ready? <enter>')

content = open('.realsync').readlines()
for hi, line in enumerate(content):
    if line.strip().startswith('host'):
        # hi stores the line number of the "host =" line
        break

fi = 2
for fi, host in enumerate(hosts, 2):
    fname = '.realsync{}'.format(fi)
    with open(fname, 'w') as f:
        content[hi] = 'host = {}\n'.format(host)
        for c in content:
            print(c, file=f, end='')
    print('replicated to', fname)
