#!/bin/bash
# symlink executables to /usr/local/bin

BIN=/usr/local/bin
# http://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ln -s $DIR/realsync $BIN/realsync
ln -s $DIR/realsync2 $BIN/realsync2
ln -s $DIR/realsync3 $BIN/realsync3
ln -s $DIR/realsync4 $BIN/realsync4
ln -s $DIR/include.py $BIN/realsync-include
ln -s $DIR/replicate_config.py $BIN/realsync-replicate
ln -s $DIR/multiplex.py $BIN/realsyncx
ln -s $DIR/multiplex.py $BIN/realsync-multiplex
