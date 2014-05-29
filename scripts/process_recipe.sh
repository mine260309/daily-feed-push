#!/bin/sh

if [ $# -lt 2 ]; then 
    echo "Invalid arguments. Usage: $0 <recipe>" >&2
    exit 1
elif [ $# -gt 2 ]; then
    echo "Invalid arguments. Usage: $0 <recipe>" >&2
    exit 1
fi

DIR=`dirname $0`
recipe=$1
out_file=$2

#filename=`basename $recipe`
#out_file=${filename%.*}_"$(date '+%Y-%m-%d')".mobi
#echo $recipe
#echo $out_file
if [ -f $out_file ]; then
  echo "mobi already exists"
  exit 0
fi

if [ -f $recipe ];
then
echo "To process $recipe"
sh $DIR/convert_feed_2_mobi.sh $recipe $out_file
else
echo "$recipe not exists!"
fi


