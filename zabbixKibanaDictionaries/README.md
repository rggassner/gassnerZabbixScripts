# zabbixKibanaDictionaries

Script to generate logstash dictionaries from zabbix host names and host groups. These data can be used in elastic search and Kibana reports.

## Description

Zabbix can sometimes be used as a inventory data source and help the reporting in other tools. This script is for extracting information from zabbix hosts and hostgroups to create data dictionaries for other reporting tools.

All interaction with Zabbix is made through [PyZabbix](https://github.com/lukecyca/pyzabbix).
## Instalation

In a debian based system:

    apt-get install python-setuptools python-dev build-essential
    easy_install pip
    pip install --upgrade virtualenv
    pip install pyzabbix

## Configuration

The following parameters are in the beginning of the zabbixKibanaDictionaries.py script file. Configure the Zabbix user that will access the API. Ensure that it has enough rights to change the hosts the hosts:

    user = "Admin"

The password for that user:

    secret = "zabbix"

The URL for the Zabbix API:

    zapi = ZabbixAPI("http://127.0.0.1/zabbix")

## Usage

Usage: zabbixKibanaDictionaries.py [options]

Options:
  -h, --help            show this help message and exit
  -t TYPE, --type=TYPE  output type: host, location, trend, environment, team,
                        service or office [default: host]

You probably will need to change the grouping regex to match your requirements.
    
Sample Dictionary output:

"127.0.0.1": Zabbix server
"192.168.1.1": Roteador Adsl


Logstash sample configuration:

filter {
	translate {
		override = true
		field => "[sflow.ReporterIP]"
		destination => "[sflow.ReporterName]"
		dictionary => "/path/to/dictionary.yaml"
	}
}

    > Written with [StackEdit](https://stackedit.io/). 