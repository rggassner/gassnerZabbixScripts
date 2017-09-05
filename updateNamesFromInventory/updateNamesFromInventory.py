#! /usr/bin/python
#pip install pyzabbix
#Updates Zabbix host name if it is an ip address
#If name from inventory has changed, update
#If repeated name, insert name after ip
#If host is in any of the predefined groups, and is repeated, disable the one with ip in the name
#Rafael Gustavo Gassner - 06/2017
from pyzabbix import ZabbixAPI
import re
#A situation you will want to disable if duplicated name is a server with multiple network addresses, for example.
disableIfDuplicatedGroups=[8,9]
user = "Admin"
secret = "zabbix"
zapi = ZabbixAPI("http://127.0.0.1/zabbix")
zapi.session.auth = (user, secret)
#zapi.session.verify = False
first=1
existsFlag=0
prog = re.compile('([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$')
isDuplicated = re.compile('([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})-.+$')
zapi.login(user, secret)
hosts=zapi.host.get(output="extend", selectInventory=True)
if not hosts:
        print ("Empty list.")
        exit()
for h in hosts:
        name=(h['name'])
        id=(h['hostid'])
        inventory=(h['inventory'])
        if inventory == []:
            continue
        print (name)
        if prog.match(name):
                if 'name' in inventory:
                        if inventory['name'] != '':
                                print (name," ",inventory['name'])
				#Verify if there is already a host with the name you will try to insert
				exists = zapi.host.get(filter={"host": inventory['name']})
				existsFlag=0
				for e in exists:
					if e['name'] == inventory['name']:
						print("Repeated name.")
						existsFlag=1
                                		zapi.host.update(hostid=id,name=name+"-"+inventory['name'])
                                		zapi.host.update(hostid=id,host=name+"-"+inventory['name'])
				if existsFlag == 0:
                                	zapi.host.update(hostid=id,name=inventory['name'])
                                	zapi.host.update(hostid=id,host=inventory['name'])
                        else:
                                print (name,"Inventory available, but name empty.")
                else:
                        print (name, "Inventory not available.")
	else: 
		#If there was an update and the name is not empty
		if (name != inventory['name']) and (inventory['name'] != ""):
			exists = zapi.host.get(filter={"host": inventory['name']})
                        existsFlag=0
                        for e in exists:
                        	if e['name'] == inventory['name']:
                                        existsFlag=1
                        if existsFlag == 0:
				print (name," ",inventory['name'], "Is not an ip address. Names differ, updating from inventory.")
                                zapi.host.update(hostid=id,name=inventory['name'])
                                zapi.host.update(hostid=id,host=inventory['name'])

print ("Disabling duplicated")
servers=zapi.host.get(groupids=disableIfDuplicatedGroups)
for r in servers:
	nameServer=(r['name'])
	idServer=(r['hostid'])
	if isDuplicated.match(nameServer):
		print (nameServer)
		zapi.host.update(hostid=int(idServer),status='1')
