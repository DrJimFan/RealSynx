#!/usr/bin/env python3
"""
Copy .realsync to .realsync2 ... .realsync<n>
"""

import os
import sys
from collections import OrderedDict

if len(sys.argv) < 2:
    print(sys.argv[0], '<file_of_host_name>')
    print('Each line can be either host_url or <id>:host_url')
    sys.exit(1)

assert os.path.exists('.realsync')
os.system('mkdir -p .realsynx')
os.system('cp .realsync .realsynx/.realsync0')
print('Original .realsync copied to .realsynx/.realsync0')

def prompt(msg):
    ans = input(msg)
    if ans.lower() in ['n', 'q']:
        sys.exit(1)

# no longer need 'clear' if we can delete .realsynx folder directly
# if sys.argv[1] == 'clear':
#     # TODO use user specified IDs
#     prompt('Do you want to clear all .realsync<n>? ".realsync" itself will be preserved: ')
#     os.system("find . -regex './.realsync[0-9][0-9]*' -delete")
#     sys.exit(0)

hosts = OrderedDict()
# ID starts from 1 because the original .realsync is copied to .realsync0
counter = 1
for l in open(sys.argv[1]):
    l = l.strip()
    if l and not l.startswith('#'):
        if ':' in l: # format <id>:url
            id, host = l.split(':')
            try:
                hosts[int(id)] = host.strip()
            except ValueError:
                raise ValueError('bad host URL spec, should be either '
                '`int_id:URL` '
                'or simply a line of `URL`: ' + l)
        else:
            host = l
            id = counter
            hosts[id] = host
            counter += 1
        print('id', id, '=>', host)
print('Creating', len(hosts), 'replicas in .realsynx/ folder')
prompt('Ready? <enter>')

content = open('.realsync').readlines()
for hi, line in enumerate(content):
    if line.strip().startswith('host'):
        # hi stores the line number of the "host =" line
        break

for fi, host in hosts.items():
    fname = '.realsynx/.realsync{}'.format(fi)
    with open(fname, 'w') as f:
        content[hi] = 'host = {}\n'.format(host)
        for c in content:
            print(c, file=f, end='')
    print('replicated to', fname)
