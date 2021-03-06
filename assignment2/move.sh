#!/bin/bash

function mover {
    echo "Starting file transfer."
    
    if [ -z $ftype ]
    then
	files=$(ls $src)
    else
	files=$(ls $src | grep ".$ftype")
    fi
    # Moving files here
    echo "Found ${#files[@]} file(s)"
    for file in $files
    do
	echo "Transfering file ${file}..."
	mv "${src}/${file}" ${dst}
    done
    echo "Done!"
}

# Check that we get at least 2 arguments from terminal
if [ "$#" -ge "2" ]
then # If we do capture the three first arguments in src, dst and ftype
    src=$1
    dst=$2
    ftype=$3
else # Else exit with an error message, chose 999
    echo "ERROR: You need to provide a source and destination directory."
    exit 999 # die with error code 999
fi

# declare an array files
declare -a files

# Check that the source directory exists
if [ ! -d "$src" ]
then
    echo "ERROR: Directory $src does not exist!"
    exit 999 # die with error code 999
# Check that destination directory exists
elif [ ! -d "$dst" ]; then
    echo "The directory $dst does not exist. Do you want to create the directory? [yes/no]"
    read answer
    case "$answer" in
	"Yes" | "yes" | "y" | "Y")
	    echo "Creating directory $dst"
	    mkdir $dst
	    mover;;
	"No" | "no" | "n" | "N" | *)
	    echo "ERROR: Directory $dst does not exist! Please create the directory before trying again."
	    exit 999 # die with error code 999
    esac
# All is good so far, lets start moving files
else
    echo "Both directories exist."
    # Check to see if the user wants to move files of a particular type
    mover
fi
