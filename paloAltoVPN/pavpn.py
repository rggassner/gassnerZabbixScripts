#! /usr/bin/python3
#Return json formatted db for zabbix low level discovery
#Rafael Gustavo Gassner - 01/2022

#apt install python3-pip
#pip3 install xmltodict
#pip3 install  py-zabbix

import requests,xmltodict,json
from datetime import datetime
from pyzabbix import ZabbixMetric, ZabbixSender
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

THIS_HOST='Zabbix server'
ZABBIX_SERVER='192.168.1.1'
WEB_SERVER=''
KEY=''

url = 'https://'+WEB_SERVER+'/api/?type=op&cmd=%3Cshow%3E%3Crunning%3E%3Ctunnel%3E%3Cflow%3E%3Call%3E%3C/all%3E%3C/flow%3E%3C/tunnel%3E%3C/running%3E%3C/show%3E&key='+KEY

packet=[]
ctime=datetime.now()
ctime=int(ctime.timestamp())
response = requests.get(url,verify=False)
data = json.loads(json.dumps(xmltodict.parse(response.content)))

#Low Level Discovery
first=True
lld='{ \"data\":['
for vpn in data['response']['result']['IPSec']['entry']:
    if first:
        first=False
    else:
        lld=lld+','
    lld=lld+'{'
    lld=lld+'"name":"'+vpn['name']+'",'
    lld=lld+'"key":"'+vpn['name']+'"'
    lld=lld+'}'
lld=lld+']}'
packet.append(ZabbixMetric(THIS_HOST,'pavpn.discovery',lld,ctime))


#Send data
for vpn in data['response']['result']['IPSec']['entry']:
    for key, value in vpn.items():
        packet.append(ZabbixMetric(THIS_HOST,'pavpn.'+key+'['+vpn['name']+']',value,ctime))
result = ZabbixSender(use_config=False,zabbix_server=ZABBIX_SERVER).send(packet)

