#!/usr/bin/env python3
"""
realsync can only exclude, not include, certain directories.
Use this script to append a list of `exclude=` to .realsync config file
You specify the dirs to INCLUDE, and this script will exclude all the other subdirs of the root dir
"""

import os
import sys

if len(sys.argv) < 3:
    print(sys.argv[0], 'root_dir realsync_config [list of include dirs ...]')
    sys.exit(1)

root, realsync, *includes = sys.argv[1:]
if '/' not in realsync:
    realsync = os.path.join(root, realsync)

includes = list(map(lambda s: s.strip("/"), includes))

print('Creating backup:', realsync+'.bak')
os.system('cp {} {}'.format(realsync, realsync+'.bak'))

for _, folders, _ in os.walk('.'):
    break

excludes = [f for f in folders if f not in includes]

with open(realsync, 'r') as f:
    contents = f.readlines()

AUTOGEN = '### AUTOGEN ###'
stripped = list(map(str.strip, contents))
if AUTOGEN in stripped:
    print('Previous AUTOGEN found, removing it')
    idx = stripped.index(AUTOGEN)
    # discard all the rest
    del contents[idx:]

with open(realsync, 'w') as f:
    for line in contents:
        f.write(line)
    f.write(AUTOGEN + '\n')
    for exc in excludes:
        f.write('exclude = {}\n'.format(exc))

print('Exclude list written to', realsync)
