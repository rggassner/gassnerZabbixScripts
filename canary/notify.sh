#!/bin/bash
#Canary file monitoring with Zabbix
#Rafael Gustavo Gassner - 03/2021
#Monitor when a file, or set of files, are accessed and upon detection
#execute several commands to help identify the source of the access.
#This script should be run by cron every minute.
#The file files2monitor should contain the files to monitor, all in one line, space separated.
#
#If you have problems using flock, you can avoid simultaneous execution with:
#* * * * *   root  lsof /opt/notify.sh || /opt/notify.sh >/dev/null 2>&1
#
#Dependencies: inotify-tools, flock, zabbix_sender
{
    flock -n 100 || exit
    maxLines=900
    sender="/usr/bin/zabbix_sender"
    conf="/etc/zabbix/zabbix_agentd.conf"
    spath="/usr/src/canary"
    $sender -c $conf -k canary.status[] -o "0" &
    inotifywait --format '%w,%-e' -m -q --fromfile $spath/files2monitor | \
        while IFS= read -r event
        do 
            echo $event
            filename=`echo $event | cut -d , -f 1`
            fevent=`echo $event | cut -d , -f 2`
            $sender -c $conf -k canary.top[] -o "`echo filename: $filename - event: $event - command: top -n -n1; top -b -n1`" &
            $sender -c $conf -k canary.lsofile[] -o "`echo filename: $filename - event: $event - command: lsof -n $filename; lsof -n $filename`" &
            $sender -c $conf -k canary.who[] -o "`echo filename: $filename - event: $event - command: who -a; who -a`" &
            for pid in `fuser $filename`
            do
                $sender -c $conf -k canary.fuser[] -o "`echo filename: $filename - event: $event - pid: $pid - command: ps -p $pid; ps -p $pid`" &
            done
            $sender -c $conf -k canary.ps[] -o "`echo filename: $filename - event: $event - command: ps -ef f; ps -ef f | head -n $maxLines`" &
            $sender -c $conf -k canary.lsof[] -o "`echo filename: $filename - event: $event - command: lsof -n; lsof -n | head -n $maxLines`" &
            $sender -c $conf -k canary.netstat[] -o "`echo filename: $filename - event: $event - command: netstat -tupan; netstat -tupan | head -n $maxLines`" &
            $sender -c $conf -k canary.status[] -o "1" &
            pkill -f "inotifywait --format %w,%-e -m -q --fromfile $spath/files2monitor"
        done
} 100>/tmp/notify.lock 
