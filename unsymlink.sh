#!/bin/bash
# remove symlink executables in /usr/local/bin

BIN=/usr/local/bin
printf "Are you sure to remove all realsync symlinks in $BIN? [y/n] "
read ans

if [ "$ans" == "y" ]; then
    rm -f $BIN/realsync*
    echo 'removed'
else
    echo 'cancelled'
fi
