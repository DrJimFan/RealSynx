#!/usr/bin/env python3
"""
Copy .realsync to .realsync2 ... .realsync<n>
"""

import os
import sys
import argparse
from collections import OrderedDict


parser = argparse.ArgumentParser()
parser.add_argument('host_name_file',
                    help='Each line can be either host_url or <id>:host_url')
parser.add_argument('-s', '--src-file', default='.realsync',
                    help='original source file to be replicated')
args = parser.parse_args()

assert os.path.exists(args.host_name_file)
assert os.path.exists(args.src_file)
print('mkdir .realsynx/')
os.system('mkdir -p .realsynx')


def prompt(msg):
    ans = input(msg)
    if ans.lower() in ['n', 'q']:
        sys.exit(1)

# no longer need 'clear' if we can delete .realsynx folder directly
# if sys.argv[1] == 'clear':
#     prompt('Do you want to clear all .realsync<n>? ".realsync" itself will be preserved: ')
#     os.system("find . -regex './.realsync[0-9][0-9]*' -delete")
#     sys.exit(0)

hosts = OrderedDict()
# ID starts from 1 because the original .realsync is copied to .realsync0
counter = 1
for l in open(args.host_name_file):
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

content = open(args.src_file).readlines()
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
