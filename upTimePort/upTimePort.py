#! /usr/bin/python
#pip install pyzabbix
#Get a list of all switches and call external report script to create reports for it.
#Rafael Gustavo Gassner - 08/07/2017
from __future__ import print_function
from pyzabbix import ZabbixAPI
import os,re,errno
import datetime
switchGroupID=8
user = "Admin"
secret = "zabbix"
community =  "public"
zapi = ZabbixAPI("http://127.0.0.1/zabbix")
reportScript = "/root/scripts/upTimePort/report.py"
outputDirectory = "/var/www/html/reports/upTimePort"
zapi.session.auth = (user, secret)
#zapi.session.verify = False
zapi.login(user, secret)
hosts=zapi.host.get(output="extend", selectInventory=True)
if not hosts:
        print ("Empty list.")
        exit()
now = datetime.datetime.now()
directory=outputDirectory+"/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"
try:
	os.makedirs(directory)
except OSError as e:
	if e.errno != errno.EEXIST:
		raise
for s in zapi.host.get(output="extend", selectInventory=True, groupids=[switchGroupID]):
	name=(s['name'])
	hostid=(s['hostid'])
	for i in zapi.hostinterface.get(hostids=[hostid],filter={"type": 2}):
		ip=(i['ip'])
		name=name.replace(" ","_")
		print (name+" "+ip)
		os.system(reportScript+" "+ip+" "+ community+" >"+directory+name+".html")
