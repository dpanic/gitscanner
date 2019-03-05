#!/bin/bash
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
echo $SCRIPTPATH
cd $SCRIPTPATH

python3 -B ../bot.py ../urls.txt >> /var/log/app.log 2>&1
 