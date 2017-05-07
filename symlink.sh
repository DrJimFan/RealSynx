#!/bin/bash
# symlink executables to /usr/local/bin

BIN=/usr/local/bin

ln -s ./realsync $BIN/realsync
ln -s ./realsync2 $BIN/realsync2
ln -s ./realsync3 $BIN/realsync3
ln -s ./realsync4 $BIN/realsync4
ln -s ./include.py $BIN/rs-include
ln -s ./replicate_config.py $BIN/rs-replicate
