#!/usr/bin/env python3
"""
Start multi realsync with .realsync1 ... .realsync<n>
"""
import os
import sys
import shlex
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('session', nargs='?', default='realsync', help='tmux session name')
parser.add_argument('--kill', nargs='?', default='no', help='kill the tmux session, default kill session="realsync"')
args = parser.parse_args()

def prompt(msg):
    ans = input(msg)
    if ans.lower() in ['n', 'q']:
        sys.exit(1)

if args.kill != 'no':
    session = 'realsync' if args.kill is None else args.kill
    prompt('Are you sure to kill session "{}"? '.format(session))
    os.system('tmux kill-session -t ' + session)
    print('session "{}" killed'.format(session))
    sys.exit()
session = args.session

assert os.path.exists('.realsync')
fnames = []
for fname in os.listdir('.'):
    if fname.startswith('.realsync') and fname != '.realsync':
        try:
            fnames.append(int(fname[len('.realsync'):]))
        except ValueError:
            print(fname, 'does not end with int. Skip.')
fnames.sort()

if not fnames:
    print('ERROR: must have at least .realsync1; run `realsync-replicate` first.')
    sys.exit(1)

for fname in fnames:
    print('Found replica config file:', '.realsync'+str(fname))

prompt('Start realsync multiplexer with tmux session "{}"? '.format(session))

def sys_run(cmd, dry=0):
    print(cmd)
    if not dry:
        os.system(cmd)

# window names will be r3, r10, etc.
win = 'r{:0>2d}'.format
sys_run('tmux new-session -s {} -n {} -d bash'.format(session, win(fnames[0])))
for fname in fnames[1:]:
    sys_run('tmux new-window -t {} -n {} bash'.format(session, win(fname)))
for fname in fnames:
    cmd = 'realsync {} .'.format(fname)
    sys_run('tmux send-keys -t {}:{} {} Enter'.format(session, win(fname), shlex.quote(cmd)))
