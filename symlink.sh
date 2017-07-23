#!/bin/bash
# symlink executables to /usr/local/bin

BIN=/usr/local/bin
# http://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ln -fs $DIR/realsync $BIN/realsync
ln -fs $DIR/realsync2 $BIN/realsync2
ln -fs $DIR/realsync3 $BIN/realsync3
ln -fs $DIR/realsync4 $BIN/realsync4
ln -fs $DIR/include.py $BIN/realsynx-include
ln -fs $DIR/replicate.py $BIN/realsynx-replicate
ln -fs $DIR/multiplex.py $BIN/realsyncx
ln -fs $DIR/multiplex.py $BIN/realsynx
