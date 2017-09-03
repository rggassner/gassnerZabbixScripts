#! /usr/bin/python
# -*- coding: utf-8 -*-
#apt-get install python-setuptools python-dev build-essential
#easy_install pip
#pip install --upgrade virtualenv
#pip install pyzabbix
#pip install ipaddress
#pip install pysnmp

#Rafael Gustavo Gassner - 06/2017

#Features:
#- Discover networks from routers that are in a zabbix group and create a Zabbix Discovery Rule including those networks.
#- Choose the max number of networks created in each discovery rule.
#- Copy checks, delay, proxy configuration and device uniqueness criteria from a template discovery rule.
#- Create html or csv router network interfaces report, including its name.
#- Include and exclude ip range options.
#- Template rule can be changed and you can run the script to update de discovery rules. All discovery rule that matches the router name pattern will be deleted and re-created.

#Documentation:
#Do not configure more than 112 maxNetPerRule or you might get into 2048 zabbix characters restriction for ip range.

from pyzabbix import ZabbixAPI
from pysnmp.hlapi import *
from pysnmp.proto import rfc1902
from optparse import OptionParser
import ipaddress

user = "Admin"
secret = "zabbix"
zapi = ZabbixAPI("http://127.0.0.1/zabbix")
community = "public"
routersGroupName="Router"
templateDiscoveryRule="TEMPLATE"
includeIfInRange=["10.0.0.0/8","172.16.0.0/12","192.168.0.0/16"]
ignoreIfInRange=["127.0.0.0/8"]
maxNetPerRule = 10
tableColor = "#FFFFFF"

parser = OptionParser()
parser.add_option("-t", "--type",
    default="html",
    help="output type: html, csv "
    "or api [default: %default]")
(options, args) = parser.parse_args()

nameCounter=0

zapi.session.auth = (user, secret)
#zapi.session.verify = False
zapi.login(user, secret)
hostgroup=zapi.hostgroup.get(filter={"name": routersGroupName})
if not hostgroup:
    print ("Host Group not found.")
    exit()

for h in hostgroup:
    groupid=h['groupid']


def isInIncludeRange(network):
	network=unicode(network,"utf-8")
	for i in includeIfInRange:
		i=unicode(i,"utf-8")
		n1 = ipaddress.ip_network(i, strict=False)
		n2 = ipaddress.ip_network(network, strict=False)
		try:
			if(len(list(n1.address_exclude(n2))) >= 0):
				return True
		except ValueError:
			pass
	return False

def isInExcludeRange(network):
	network=unicode(network,"utf-8")
	for i in ignoreIfInRange:
		i=unicode(i,"utf-8")
		n1 = ipaddress.ip_network(i, strict=False)
		n2 = ipaddress.ip_network(network, strict=False)
		try:
			if(len(list(n1.address_exclude(n2))) >= 0):
				return True
		except ValueError:
			pass
	return False

def netmask_to_cidr(netmask):
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

def getDescription(router,community,id):
    errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
    CommunityData(community),
    UdpTransportTarget((router, 161)),
    ContextData(),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2.'+str(id))),lexicographicMode=False)
    )
    if errorIndication:
        #print(errorIndication)
        #break
        return "NoDescription"
    elif errorStatus:
        #print('%s at %s' % (errorStatus.prettyPrint(),
        #errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        #break
        return "No Description"
    else:
        for varBind in varBinds:
            return varBind[1]

def print_html_header():
    print ("<html><head>")
    print ("<link rel=\"stylesheet\" type=\"text/css\" href=\"http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.10.5/css/jquery.dataTables.css\">")
    print ("</head><body>")
    print ("<table id=\"ipInventory\" class=\"cell-border compact\" cellspacing=\"0\" width=\"100%\"><thead><tr><th>Router</th><th>Id-Name</th><th>Ip/Mask</th></tr></thead>")
    print ("<tfoot><tr><th>Router</th><th>Id-Name</th><th>Ip/Mask</th></tr></tfoot><tbody>")

def print_body(rtype):
    hosts=zapi.host.get(selectInventory=True)
    if not hosts:
        print ("Empty list.")
        exit()
    for s in zapi.host.get(output="extend", groupids=[groupid]):
	name=(s['name'])
	hostid=(s['hostid'])
	for i in zapi.hostinterface.get(hostids=[hostid],filter={"type": 2}):
		ip=(i['ip'])
		name=name.replace(" ","_")
                gen_report(ip,community,name,rtype)

def print_html_footer():
    print ("</tbody></table>")
    print ("  <script type=\"text/javascript\" charset=\"utf8\" src=\"http://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.2.1.min.js\"></script>")
    print ("  <script type=\"text/javascript\" charset=\"utf8\" src=\"http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.10.5/jquery.dataTables.min.js\"></script>")
    print ("<script>")
    print (" $(function(){")
    print ("    $(\"#ipInventory\").dataTable(")
    print ("{")
    print ("\"rowCallback\": function( row, data, index ) {")
    print ("    if ( \"5\" == \"5\" )")
    print ("    {")
    print ("        $('td', row).css('background-color', '"+tableColor+"');")
    print ("    }")
    print ("}")
    print ("}")
    print (");")
    print ("  })")
    print ("        </script>")
    print ("</body></html>")

#Delete all existing discovery rules that match ROUTER-* pattern
def delete_existing_rules(name):
	rname=name+"-*"
	actual=zapi.drule.get(search={"name": rname}, searchWildcardsEnabled=True)
    	for a in actual:
        	zapi.drule.delete(a['druleid'])

#Main routine
def gen_report(router, community, name, rtype):
    global nameCounter
    rcounter=0
    ipRange=""
    delete_existing_rules(name)
    for (errorIndication,
        errorStatus,
        errorIndex,
        varBinds) in nextCmd(SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((router, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.4.20.1.1')),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.4.20.1.2')),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.4.20.1.3')),
            lexicographicMode=False):
        if errorIndication:
            #print(errorIndication)
            break
        elif errorStatus:
            #print('%s at %s' % (errorStatus.prettyPrint(),
            #    errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
            break
        else:
            zipped = zip(varBinds[0::3],varBinds[1::3],varBinds[2::3])
            for ((t,ip),(t,id),(t,mask)) in zipped:
                description=getDescription(router,community,id)
                if (rtype == "html"):
	            print ("<tr><td>"+str(name)+"</td><td>"+str(id)+"-"+str(description)+"</td><td>"+rfc1902.IpAddress.prettyPrint(ip)+"/"+str(netmask_to_cidr(rfc1902.IpAddress.prettyPrint(mask))) +"</td></tr>")
                elif (rtype == "csv"):
	            print (str(name)+","+str(id)+"-"+str(description)+","+rfc1902.IpAddress.prettyPrint(ip)+"/"+str(netmask_to_cidr(rfc1902.IpAddress.prettyPrint(mask))))
                elif ((rtype == "api") and (netmask_to_cidr(rfc1902.IpAddress.prettyPrint(mask))!=32) and (netmask_to_cidr(rfc1902.IpAddress.prettyPrint(mask)) >=16 ) and isInIncludeRange(rfc1902.IpAddress.prettyPrint(ip)+"/"+str(netmask_to_cidr(rfc1902.IpAddress.prettyPrint(mask)))) and not (isInExcludeRange(rfc1902.IpAddress.prettyPrint(ip)+"/"+str(netmask_to_cidr(rfc1902.IpAddress.prettyPrint(mask))))) ):
                    if(rcounter==0):
                        ipRange=rfc1902.IpAddress.prettyPrint(ip)+"/"+str(netmask_to_cidr(rfc1902.IpAddress.prettyPrint(mask)))
                    else:
                        ipRange=ipRange+","+rfc1902.IpAddress.prettyPrint(ip)+"/"+str(netmask_to_cidr(rfc1902.IpAddress.prettyPrint(mask)))
		    rcounter=rcounter+1
		    if (rcounter==maxNetPerRule):
		    	update_discovery(name,ipRange)
			ipRange=""
			rcounter=0
    if ((rtype == "api") and (rcounter != 0)):
    	update_discovery(name,ipRange)
	ipRange=""
	rcounter=0
	nameCounter=0

def update_discovery(dname,ipRange):
    global nameCounter
    template=zapi.drule.get(output="extend", selectDChecks="extend", filter={"name": templateDiscoveryRule})
    if not template:
        print ("Discovery rule template not found.")
        exit()
    for t in template:
        templateid=t['druleid']
    t['iprange']=ipRange
    t['name']=dname+"-"+str(nameCounter)
    #To create enabled, set status 0
    t['status']="1"
    zapi.drule.create(t)
    nameCounter=nameCounter+1   

if (options.type=="html"):
    print_html_header()
    print_body(options.type)
    print_html_footer()
elif (options.type=="csv"):
    print_body(options.type)
elif (options.type=="api"):
    print_body(options.type)
