#!/bin/sh

if [ $# -ne 2 ]; then
    echo "Invalid arguments. Usage: $0 <recipe> <mobi>" >&2
    exit 1
fi

DIR=`dirname $0`
recipe=$1
mobi=$2

if [ -f $mobi ]; then
  echo "mobi already exists"
  exit 0
fi

if [ -f $recipe ];
then
  echo "To process $recipe"
  sh $DIR/convert_feed_2_mobi.sh $recipe $mobi
else
  echo "$recipe not exists!"
  exit 1
fi


