This script activelly scans arp and sends to zabbix server using zabbix_sender.

# Installing on monitoring host:

- Install arp-scan
- Install zabbix-sender
- Install and configure zabbix-agent
- Configure "interfaces" variable in arpMonitoring.sh
- Set crontab to run the arpMonitoring.sh every ten minutes or so.

# Configurations on Zabbix-Server:

- Import Template ARP Monitoring.xml into the templates
- Associate the template with the host that will monitor arp.

Run some times manually so Zabbix will create the LLD items and start populating them.

With the script and template, you will be able to:
 - Detect newly connected devices on the network.
 - Have a history of which macs were used by which ips and the other way around.
 - Detect if there are multiple ips associated to the same mac.
 - Detect if there are multiple macs associated to the same ip address.
 - Identify the active period on the network for each device.
 
Since this is designed for a small environment, the trigger for new device has no recovery expression, and should be manually disabled.

You can configure the "new device" trigger disabled for initial run.

After that you could disable each trigger mannualy when you have recognized the new device as not beeing a rogue one.

In the zabbix template, "Allowed hosts" variable should be configured for your environment in item prototypes and in discovery rule.
