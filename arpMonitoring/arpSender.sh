#!/bin/bash
#Rafael Gustavo Gassner 02/2021
#This script activelly scans arp and sends to zabbix server using zabbix_sender.
#arp-scan should be installed and interfaces variable should
# be configured for your environment.
#You will want to run every 10 minutes or so, using crontab.
#First run(s) might not populate data, since LLD items
# are still beeing created in zabbix server.
#With the script and template, you will be able to:
# - Detect newly connected devices on the network.
# - Have a history of which macs were used by which ips and the other way around.
# - Detect if there are multiple ips associated to the same mac.
# - Detect if there are multiple macs associated to the same ip address.
# - Identify the active period on the network for each device.
#Since this is designed for a small environment, the trigger for
#new device has no recovery expression, and should be manually disabled.
#You can configure the "new device" trigger disabled for initial run.
#After that you could disable each trigger mannualy when you have
#recognized the new device as not beeing a rogue one.
#In the zabbix template, "Allowed hosts" variable should be configured
# for your environment in item prototypes and in discovery rule.

interfaces="eth0.1 eth0.2"
zabbix_conf="/etc/zabbix/zabbix_agentd.conf"
arp_scan="/usr/sbin/arp-scan"
sender="/usr/bin/zabbix_sender"

fullData=`for iface in $interfaces
do
        $arp_scan --localnet --interface=$iface -q -x
done`
IFS=$'\n'
first=1
lld="{ \"data\":["
for entry in $fullData
do
        if [[ first -eq 0 ]]
        then
                lld="${lld},"
        else
                first=0
        fi
        ipAddress=`echo $entry | awk '{print $1}'`
        HWAddress=`echo $entry | awk '{print $2}'`
        lld="${lld}{"
        lld="${lld}\"ipAddress\":\"${ipAddress}\","
        lld="${lld}\"HWAddress\":\"${HWAddress}\""
        lld="${lld}}"
done
lld="${lld}]}"
$sender -c $zabbix_conf -k arp.discovery -o $lld
for mac in `echo "$fullData" | awk '{print $2}'| sort | uniq`
do
        ips=`echo "$fullData" | grep "$mac" | awk '{print $1}' | tr '\n' ' '`
        $sender -c $zabbix_conf -k arp.macIps[$mac] -o $ips
done
for ip in `echo "$fullData" | awk '{print $1}'| sort | uniq`
do
        macs=`echo "$fullData" | grep -P "^${ip}\t" | awk '{print $2}' | tr '\n' ' '`
        $sender -c $zabbix_conf -k arp.ipMacs[$ip] -o $macs
done
for line in $fullData
do
        mac=`echo "$line" | awk {'print $2'}`
        nIp=`echo "$fullData" | grep "${mac}" | wc -l`
        $sender -c $zabbix_conf -k arp.ipCount[$mac] -o $nIp
done
for line in $fullData
do
        ip=`echo "$line" | awk {'print $1'}`
        nMac=`echo "$fullData" | grep -P "^${ip}\t" | wc -l`
        $sender -c $zabbix_conf -k arp.macCount[$ip] -o $nMac
done
