Monitor when a file, or set of files, are accessed and upon detection execute several commands to help identify the source of the access.
This script should be run by cron every minute.
The file files2monitor should contain the files to monitor, all in one line, space separated.
Dependencies: inotify-tools, flock, zabbix_sender
