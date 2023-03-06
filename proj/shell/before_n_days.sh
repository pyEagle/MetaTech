#! /bin/bash

i=0
start_day='20210824'
end_str='20210601'
while [ $start_day -ge $end_str ];do
    echo $start_day
    i=`expr $i + 1`
    start_day=`date --date="$start_day $i days ago" +"%Y%m%d"`
done