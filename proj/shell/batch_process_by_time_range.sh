#! /bin/bash

start_day='20210824'
end_day='20210718'
while :;do
    i=0
    while :;do
        d=`date --date="$start_day $i days ago" +"%Y%m%d"`
        if [[ $d < $end_day ]];then
            break
        fi

        echo $d

        ((i++))
        if [[ $i -ge 10 ]];then
            break
        fi
    done

    wait # waiting for sub_process finish
    start_day=`date --date="$start_day $i days ago" +"%Y%m%d"`
    if [[ $start_day < $end_day ]];then
        break
    fi
done
