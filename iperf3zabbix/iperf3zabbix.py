#!venv/bin/python
import iperf3
import json
from zabbix_utils import Sender
ZABBIX_SERVER = {"server": "192.168.1.1","port": 10051}
sender = Sender(**ZABBIX_SERVER)
host='VPN'
client = iperf3.Client()
client.duration = 3
client.intervals = 3
client.server_hostname = '192.168.1.100'
client.port = 5201
result = client.run()
directions=['sum_sent','sum_received']
attributes=['bits_per_second','retransmits']
data = json.loads(str(result))
for direction in directions:
    for attribute in attributes:
        if attribute in data['end'][direction]:
            print('{} {}'.format('iperf3.'+direction+'.'+attribute,data['end'][direction][attribute]))
            response = sender.send_value(host,'iperf3.'+direction+'.'+attribute,data['end'][direction][attribute])
            if response.failed == 0:
                print(f"Value sent successfully in {response.time}")
            else:
                print("Failed to send value")

