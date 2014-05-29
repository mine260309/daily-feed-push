#!/bin/sh

if [ $# -lt 2 ]; then 
    echo "Invalid arguments. Usage: $0 <recipe> <out-file>" >&2
    exit 1
elif [ $# -gt 2 ]; then
    echo "Invalid arguments. Usage: $0 <recipe> <out-file>" >&2
    exit 1
fi

ebook-convert $1 $2
