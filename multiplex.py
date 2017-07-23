#!/usr/bin/env python3
"""
Start multi realsync with .realsync0 (original .realsync), .realsync1, ... .realsync<n>
"""
import os
import sys
import shlex
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('realsync_ids', nargs='?', default='all', help="""
                        'all': all .realsynx/.realsync<n> configs
                        2-7: a range of ids, both ends inclusive
                        2,5,9: comma separated
                        1-100^42-45: exclude a range of numbers
                        1-100^42^52^62: exclude a few numbers
                        1-6,3-8,100: mixture of range and commas
                        1-100^42^55,301,305,400-500^420-430: arbitrarily complicated ranges
                    """)
parser.add_argument('-k', '--kill', nargs='?', default='no', help='kill the tmux session, default kill session="realsync"')
parser.add_argument('-s', '--session', default=None, help='tmux session name. Default to realsync-<current-time-HMS>')
parser.add_argument('-d', '--dry-run', action='store_true')
args = parser.parse_args()

DEBUG = args.dry_run

if DEBUG:
    print('======= dry run =======')

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

if args.session is not None:
    session = args.session
else:
    import datetime
    session = 'realsync-' + datetime.datetime.now().strftime('%H_%M_%S')

def parse_nums(spec):
    """
    2-7: a range of ids, both ends inclusive
    2,5,9: comma separated
    1-100^42-45: exclude a range of numbers
    1-100^42^52^62: exclude a few numbers
    1-6,3-8,100: mixture of range and commas
    1-100^42^55,301,305,400-500^420-430: arbitrarily complicated ranges
    """
    spec = spec.strip()
    try:
        if ',' in spec:
            nums = []
            for sub in spec.split(','):
                nums.extend(parse_nums(sub))
            # remove duplicates
            return sorted(list(set(nums)))
        elif '^' in spec:
            # everything after the first ^ are to be excluded
            subs = spec.split('^')
            assert len(subs) >= 2, '[initial]^[exclude]'
            include = set(parse_nums(subs[0]))
            for sub in subs[1:]:
                include -= set(parse_nums(sub))
            return sorted(list(include))
        elif '-' in spec:
            ends = list(map(int, filter(None, spec.split('-'))))
            assert len(ends) == 2, 'range `x-y` must have exactly one hyphen: '+spec
            assert ends[0] <= ends[1], 'end point must >= start point: '+spec
            return list(range(ends[0], ends[1]+1))
        else:
            return [int(spec)]
    except ValueError:
        raise ValueError('Invalid number spec. Example: 1-100^42^55,200-300,309')


assert os.path.exists('.realsync')
assert os.path.exists('.realsynx/'), \
    '.realsynx/ dir must exist. Run `realsync-replicate` first'

if args.realsync_ids == 'all':
    fnames = []
    for fname in os.listdir('.realsynx'):
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
        f = '.realsynx/.realsync{}'.format(fname)
        assert os.path.exists(f), '{} does not exist.'.format(f)
    

for fname in fnames:
    print('Found replica config file: .realsync'+str(fname))

prompt('Start realsynx multiplexer with tmux session "{}"? '.format(session))

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
    # our improved `realsync` script will recognize config files under .realsynx/ folder
    # e.g. `realsync 42` will find the file .realsynx/.realsync42
    cmd = 'realsync {} .'.format(fname)
    # two enters to start replication on realsync prompt
    sys_run('tmux send-keys -t {}:{} {} Enter Enter'.format(session, win(fname), shlex.quote(cmd)))
