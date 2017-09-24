#!/usr/bin/python
#apt-get install python-pip
#pip install pysnmp-apps
#yum install python-devel pysnmp-mibs
#pip install pysnmp==4.3.0
#Rafael Gustavo Gassner - 07/2017

import datetime 
import sys
from pysnmp.hlapi import *
switch=sys.argv[1]
comunidade=sys.argv[2]

#seconds * 100
#1 month = 259200000
target=259200000 

 
def duration_human(seconds):
    seconds = long(round(seconds))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365.242199)
 
    minutes = long(minutes)
    hours = long(hours)
    days = long(days)
    years = long(years)
 
    duration = []
    if years > 0:
        duration.append('%d year' % years + 's'*(years != 1))
    else:
        if days > 0:
            duration.append('%d day' % days + 's'*(days != 1))
        if hours > 0:
            duration.append('%d hour' % hours + 's'*(hours != 1))
        if minutes > 0:
            duration.append('%d minute' % minutes + 's'*(minutes != 1))
        if seconds > 0:
            duration.append('%d second' % seconds + 's'*(seconds != 1))
    return ' '.join(duration)

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData(comunidade),
           UdpTransportTarget((switch, 161)),
           ContextData(),
           ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')),lexicographicMode=False)
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
	uptime=varBind[1]

print ("<html>Uptime:"+duration_human(uptime/100)+"<br><table border=1>")
print ("<tr><td>Alias</td><td>Description</td><td>Time without use</td></tr>")

for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in nextCmd(SnmpEngine(),
                          CommunityData(comunidade),
                          UdpTransportTarget((switch, 161)),
                          ContextData(),
                          ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2')),
                          ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.8')),
                          ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.9')),
                          ObjectType(ObjectIdentity('1.3.6.1.2.1.31.1.1.1.18')),
                          lexicographicMode=False):

    if errorIndication:
        print(errorIndication)
        break
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
        break
    else:
	zipped = zip(varBinds[0::4],varBinds[1::4],varBinds[2::4],varBinds[3::4])
	for ((t,description),(t,status),(t,iuptime),(t,alias)) in zipped:
		if ((iuptime>0) and (iuptime<uptime)):
			downtime=uptime-iuptime
			if ((status==2) and (downtime>target)):
				print ("<tr><td>"+alias+"</td><td>"+description+"</td><td>"+duration_human(downtime/100)+"</td></tr>")
print("</table></html>")

