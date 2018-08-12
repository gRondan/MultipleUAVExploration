import subprocess
import ipaddress
from subprocess import Popen, PIPE

network = ipaddress.ip_network('172.16.138.128/29')

for i in network.hosts():
	i = str(i)
	toping = Popen(['ping', '-c', '1', '-w', '1', i], stdout=PIPE)
	output = toping.communicate()[0]
	hostalive = toping.returncode
	if hostalive == 0:
		print(i, 'IS REACHABLE')
	else:
		print(i, 'is unreachable')
