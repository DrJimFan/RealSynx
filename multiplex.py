#!/usr/bin/env python3
"""
Start multi realsync with .realsync0 (original .realsync), .realsync1, ... .realsync<n>
"""
import os
import sys
import shlex
import argparse

DEBUG = 0

parser = argparse.ArgumentParser()
parser.add_argument('realsync_ids', nargs='?', default='all', help="""
                        'all': all ./realsync<n> configs
                        2-7: a range of ids, both ends inclusive
                        2,5,9: comma separated
                        1-6,3-8,100: mixture of range and commas
                    """)
parser.add_argument('-k', '--kill', nargs='?', default='no', help='kill the tmux session, default kill session="realsync"')
parser.add_argument('-s', '--session', nargs='?', default='realsync', help='tmux session name')
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

def parse_nums(spec):
    """
    2-7: a range of ids, both ends inclusive
    2,5,9: comma separated
    1-6,3-8,100: mixture of range and commas
    """
    spec = spec.strip()
    if ',' in spec:
        nums = []
        for sub in spec.split(','):
            nums.extend(parse_nums(sub))
        # remove duplicates
        return sorted(list(set(nums)))
    elif '-' in spec:
        ends = list(map(int, filter(None, spec.split('-'))))
        assert len(ends) == 2, 'range `x-y` must have exactly one hyphen: '+spec
        assert ends[0] <= ends[1], 'end point must >= start point: '+spec
        return list(range(ends[0], ends[1]+1))
    else:
        return [int(spec)]
            

assert os.path.exists('.realsync')


if args.realsync_ids == 'all':
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
else: # user-specified ranges of id
    # sift through fnames
    fnames = parse_nums(args.realsync_ids)
    for fname in fnames:
        f = '.realsync{}'.format(fname)
        assert os.path.exists(f), '{} does not exist.'.format(f)
    

for fname in fnames:
    print('Found replica config file:', '.realsync'+str(fname))

prompt('Start realsync multiplexer with tmux session "{}"? '.format(session))

def sys_run(cmd):
    print(cmd)
    if not DEBUG:
        os.system(cmd)

# window names will be r3, r10, etc.
win = 'r{:0>2d}'.format
sys_run('tmux new-session -s {} -n {} -d bash'.format(session, win(fnames[0])))
for fname in fnames[1:]:
    sys_run('tmux new-window -t {} -n {} bash'.format(session, win(fname)))
for fname in fnames:
    cmd = 'realsync {} .'.format(fname)
    sys_run('tmux send-keys -t {}:{} {} Enter'.format(session, win(fname), shlex.quote(cmd)))
