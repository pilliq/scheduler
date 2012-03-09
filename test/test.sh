#!/usr/bin/env bash

arg="-a"
while getopts ":a:b:c" opt; 
do
    case $opt in 
        a)
            arg="-a"
            ;;
        b)
            arg="-b"
            ;;
        c)
            arg="-c"
            ;;
    esac
done

for i in $(ls | grep -v sched | grep -v test.sh);
do 
    ../scheduler $arg < $i > sched_$i
done
exit 0
