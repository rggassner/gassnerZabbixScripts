Monitor when a file, or set of files, are accessed and upon detection execute several commands to help identify the source of the access.

This script should be run by cron every minute.

The file files2monitor should contain the files to monitor, all in one line, space separated.

Dependencies: inotify-tools, flock, zabbix_sender

## canary

Script and Zabbix template to:
 - Detect actions on canary files, read, write or open.
 - Support for multiple files monitoring.
 - Avoid multiple simultaneous execution of the script using flock.
 - Sends information to zabbix only when incident happens, for monitoring resource optimization.
 - Records information from inotify, top, netstat, lsof, who, ps and fuser upon event detection.
 - Dependencies: inotify-tools, flock, zabbix_sender
