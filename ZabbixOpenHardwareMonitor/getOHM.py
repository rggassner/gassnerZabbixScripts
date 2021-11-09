import csv
from datetime import datetime
from pyzabbix import ZabbixMetric, ZabbixSender
#Be sure to use the same name configured for the host in zabbix server
THIS_HOST='DESKTOP'
ZABBIX_SERVER='192.168.1.1'
packet=[]
now = datetime.now()

#Read csv file
with open('OpenHardwareMonitorLog-'+str(now.year)+'-'+str(now.strftime("%m"))+'-'+str(now.strftime("%d"))+'.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for i, row in enumerate(reader):
        if i == 0:
            header1=row    
        if i == 1:
            header2=row
        last=row
ctime=datetime.strptime(last[0],'%m/%d/%Y %H:%M:%S')
ctime=int(ctime.timestamp())

#Low Level Discovery
first=True
lld='{ \"data\":['
for i, col in enumerate(header1):
    part1=col.replace('/','.').replace(' ','.')
    part2=header2[i].replace('/','.').replace(' ','.')
    if part2 != "Time":
        if first:
            first=False
        else:
            lld=lld+','
        lld=lld+'{'
        lld=lld+'"name":"'+col+' '+header2[i]+'",'
        lld=lld+'"key":"'+part1+'-'+part2+'"'
        lld=lld+'}'
lld=lld+']}'
packet.append(ZabbixMetric(THIS_HOST,'ohm.discovery',lld,ctime))

#Send data
for i, col in enumerate(header1):
    part1=col.replace('/','.').replace(' ','.')
    part2=header2[i].replace('/','.').replace(' ','.')
    if part2 != "Time":
        packet.append(ZabbixMetric(THIS_HOST,'ohm.metric['+part1+"-"+part2+']',last[i],ctime))
result = ZabbixSender(use_config=False,zabbix_server=ZABBIX_SERVER).send(packet)
