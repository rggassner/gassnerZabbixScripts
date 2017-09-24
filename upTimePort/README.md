# upTimePort

Script to generate one report for each switch in a given Zabbix group, and show all ports that are without use for more than a time period.

## Description

Sometimes you run out of switches ports, and ask yourself if all of them are really in use. This script will generate a report showing which ports are without use for a determined period.

## Instalation

In a debian based system:

    apt-get install python-setuptools python-dev build-essential
    easy_install pip
    pip install --upgrade virtualenv
    pip install pyzabbix
    pip install pysnmp-apps
    pip install pysnmp==4.3.0
    yum install python-devel pysnmp-mibs


## Configuration

The following parameters are in the beginning of the upTimePort.py script file. Configure the Zabbix user that will run the script. Ensure that it has enough rights to see the hosts and to create the discovery rules:

    user = "Admin"

The password for that user:

    secret = "zabbix"

The URL for the Zabbix API:

    zapi = ZabbixAPI("http://127.0.0.1/zabbix")

The SNMP community to access the devices:

    community = "public"

The id of the Zabbix host group to get the device information:

    switchGroupID="8"

The path to the reporting script:

	reportScript = "/root/scripts/upTimePort/report.py"

The report output directory:

	outputDirectory = "/var/www/html/reports/upTimePort"

You can configure how long a port must be down to be shown in the reports in the script report.py:

	#seconds * 100
	target=259200000

## Usage

     ./upTimePort.py

	This script takes no parameters.

    > Written with [StackEdit](https://stackedit.io/). 










