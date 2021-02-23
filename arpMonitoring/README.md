This script activelly scans arp and sends to zabbix server using zabbix_sender.

arp-scan should be installed and interfaces variable should be configured for your environment.

You will want to run every 10 minutes or so, using crontab.

First run(s) might not populate data, since LLD items are still beeing created in zabbix server.

With the script and template, you will be able to:
 - Detect newly connected devices on the network.
 - Have a history of which macs were used by which ips and vice versa.
 - Detect if there are multiple ips associated to the same mac.
 - Detect if there are multiple macs associated to the same ip address.
 - Identify the active period on the network for each device.
 
Since this is designed for a small environment, the trigger for new device has no recovery expression, and should be manually disabled.

You can configure the "new device" trigger disabled for initial run.

After that you could disable each trigger mannualy when you have recognized the new device as not beeing a rogue one.

In the zabbix template, "Allowed hosts" variable should be configured for your environment in item prototypes and in discovery rule.
