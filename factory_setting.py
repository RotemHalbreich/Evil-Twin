import os

try:
	os.remove("hostapd.conf")
except OSError:
	print("Error: can't remove file")
os.system('service NetworkManager start')
os.system('service apache2 stop')
os.system('service hostapd stop')
os.system('service dnsmasq stop')
os.system('service rpcbind stop')
os.system('killall dnsmasq')
os.system('killall hostapd')
### Enable and start all the process that uses port 53.
os.system('systemctl enable systemd-resolved.service') 
os.system('systemctl start systemd-resolved')