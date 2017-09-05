# updateNamesFromInventory

This script has been developed to help fast Zabbix deploying, updating names from inventory field.

## Description

Zabbix has a useful network discovery feature, but if you have to manually rename the discovered hosts, that would take too much time on a large environment.
This script tries to solve this issue. It will copy the host name from inventory to the actual host name. You will want to configure automatic inventory for all hosts in you Discovery actions.

All interaction with Zabbix is made through [PyZabbix](https://github.com/lukecyca/pyzabbix). Sometimes hosts have multiple interfaces, like servers, routers, firewalls, and are discovered more than once, and to save resources, only one of them should be monitored. You can configure a list of groups which hosts should be disabled if they have the same name.

## Instalation

In a debian based system:

    apt-get install python-setuptools python-dev build-essential
    easy_install pip
    pip install --upgrade virtualenv
    pip install pyzabbix

## Configuration

The following parameters are in the beginning of the updateNamesFromInventory.py script file. Configure the Zabbix user that will access the API. Ensure that it has enough rights to change the hosts the hosts:

    user = "Admin"

The password for that user:

    secret = "zabbix"

The URL for the Zabbix API:

    zapi = ZabbixAPI("http://127.0.0.1/zabbix")

The ids of the hosts groups which should be disabled if repeated:

    disableIfDuplicatedGroups=[8,9]

## Usage

     ./updateNamesFromInventory.py

This script has no parameters
    
    > Written with [StackEdit](https://stackedit.io/). 