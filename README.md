# gassnerZabbixScripts
Scripts related to Zabbix

## ipDiscovery

This script has been developed to help fast Zabbix deploying, collecting SNMP data from network routers, and automatically creating discovery rules. It is also able to output csv and html reports.

## updateNamesFromInventory

Zabbix automatic network discovery inserts an IP address, or the reverse resolved name at the moment of the discovery in the name of the host. This script copies the content from the "Name" inventory field to the host field. When two identical names are identified, ip address is inserted in the beggining of the name and host is kept enable. It is possible to configure that when the host belongs to some groups, it also should be disabled. If name in inventory changes, even the host name is not an IP address, it will be updated.

## zabbixKibanaDictionaries

Script to generate logstash dictionaries from zabbix host names and host groups. These data can be used in elastic search and Kibana reports.

## upTimePort

Script to generate one report for each switch in a given Zabbix group, and show all ports that are without use for more than a time period.

