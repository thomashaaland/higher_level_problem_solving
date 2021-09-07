#!/bin/bash -x

src=$1
dst=$2

if [ ! -d "$src" ]
then
	echo "Directory $src does NOT exist!"
	exit 9999 # die with error code 9999
else if [ ! -d "$dst" ]
then
	echo "Directory $dst does NOT exist!"
	exit 9999 # die with error code 999
else
	echo "Both directories exist."
	mv ${src}* ${dst}
fi

