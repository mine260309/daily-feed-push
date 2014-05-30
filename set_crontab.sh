#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cronscript="$DIR/run.sh #Daily-feed-push"

# Add script to crontab
tmp=${TMPDIR:-/tmp}/xyz.$$
trap "rm -f $tmp; exit 1" 0 1 2 3 13 15
# Capture crontab; delete old entry
crontab -l | sed '/#Daily-feed-push/d' > $tmp
# Execute at 6:00 every day
echo "13 15 * * * $cronscript" >> $tmp
crontab < $tmp
rm -f $tmp
trap 0
