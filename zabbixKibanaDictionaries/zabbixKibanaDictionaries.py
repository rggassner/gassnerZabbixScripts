#! /usr/bin/python
# -*- coding: utf-8 -*-
#pip install pyzabbix

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from pyzabbix import ZabbixAPI
import os,re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--type",
    default="host",
    help="output type: host, location, trend, environment, team, "
    "service or office [default: %default]")
(options, args) = parser.parse_args()

user = "Admin"
secret = "zabbix"
zapi = ZabbixAPI("http://127.0.0.1/zabbix")
ips = {}
isTeam = re.compile('^Equipe - .*$')
isType = re.compile('^Tipo - .*$')
isLocation = re.compile('^Localidade - .*$')
isOffice = re.compile('^Unidade - .*$')
isService = re.compile('^Servi.* - .*$')
isTrend = re.compile('^Marca - .*$')
isEnvironment = re.compile('^Ambiente - .*$')
zapi.session.auth = (user, secret)
zapi.login(user, secret)
hosts=zapi.host.get()
if not hosts:
        print ("Empty list.")
        exit()
for h in hosts:
        name=(h['name'])
        status=(h['status'])
        hostId=(h['hostid'])
	#filter enabled hosts
	if (status == "0" ) or (status == "1"):
		if (options.type == "host"):
			ifaces=zapi.hostinterface.get(hostids=[hostId])
			for iface in ifaces:
				ips={iface['ip']:"1"}
			for key in ips:
				print ("\""+key+"\": "+name)
				break
			ips={}
		if (options.type == "location"):
			ifaces=zapi.hostinterface.get(hostids=[hostId])
			for iface in ifaces:
				ips={iface['ip']:"1"}
			for key in ips:
				groups=zapi.hostgroup.get(hostids=[hostId])
				for g in groups:
        				if isLocation.match(g['name']):
						print ("\""+key+"\": "+(g['name']).split(" ",2)[2])
						break
			ips={}
		if (options.type == "trend"):
			ifaces=zapi.hostinterface.get(hostids=[hostId])
			for iface in ifaces:
				ips={iface['ip']:"1"}
			for key in ips:
				groups=zapi.hostgroup.get(hostids=[hostId])
				for g in groups:
        				if isTrend.match(g['name']):
						print ("\""+key+"\": "+(g['name']).split(" ",2)[2])
						break
			ips={}
		if (options.type == "team"):
			ifaces=zapi.hostinterface.get(hostids=[hostId])
			for iface in ifaces:
				ips={iface['ip']:"1"}
			for key in ips:
				groups=zapi.hostgroup.get(hostids=[hostId])
				for g in groups:
        				if isTeam.match(g['name']):
						print ("\""+key+"\": "+(g['name']).split(" ",2)[2])
						break
			ips={}
		if (options.type == "type"):
			ifaces=zapi.hostinterface.get(hostids=[hostId])
			for iface in ifaces:
				ips={iface['ip']:"1"}
			for key in ips:
				groups=zapi.hostgroup.get(hostids=[hostId])
				for g in groups:
        				if isType.match(g['name']):
						print ("\""+key+"\": "+(g['name']).split(" ",2)[2])
						break
			ips={}
		if (options.type == "environment"):
			ifaces=zapi.hostinterface.get(hostids=[hostId])
			for iface in ifaces:
				ips={iface['ip']:"1"}
			for key in ips:
				groups=zapi.hostgroup.get(hostids=[hostId])
				for g in groups:
        				if isEnvironment.match(g['name']):
						print ("\""+key+"\": "+(g['name']).split(" ",2)[2])
						break
			ips={}
		if (options.type == "office"):
			ifaces=zapi.hostinterface.get(hostids=[hostId])
			for iface in ifaces:
				ips={iface['ip']:"1"}
			for key in ips:
				groups=zapi.hostgroup.get(hostids=[hostId])
				for g in groups:
        				if isOffice.match(g['name']):
						print ("\""+key+"\": "+(g['name']).split(" ",2)[2])
						break
			ips={}
		if (options.type == "service"):
			ifaces=zapi.hostinterface.get(hostids=[hostId])
			for iface in ifaces:
				ips={iface['ip']:"1"}
			for key in ips:
				groups=zapi.hostgroup.get(hostids=[hostId])
				for g in groups:
        				if isService.match(g['name']):
						print ("\""+key+"\": "+(g['name']).split(" ",2)[2])
						break
			ips={}
