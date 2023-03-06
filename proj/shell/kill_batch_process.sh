#! /bin/bash

process_name=$1

ps -ef|grep $process_name |grep -v grep |awk -'{print $2}' |xargs kill -9
