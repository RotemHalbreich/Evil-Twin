import os
import sys
import threading
import time



 


### Reset all the setting before we satrt. 
def reset_setting():
	### Start system network service
	os.system('service NetworkManager start')
	### Stop apache2 service
	os.system('service apache2 stop')
	### Stop and kill the hostapd and dnsmasq services.
	os.system('service hostapd stop')
	os.system('service dnsmasq stop')
	os.system('service rpcbind stop')
	os.system('killall dnsmasq')
	os.system('killall hostapd')
	### Enable and start all the process that uses port 53.
	os.system('systemctl enable systemd-resolved.service') 
	os.system('systemctl start systemd-resolved')  


### Delete the hostapd and dnsmasq configuration files (they were temp files).
def remove_conf_files():
	try:
	    os.remove("dnsmasq.conf")
	except OSError:
	    pass
	try:
	    os.remove("hostapd.conf")
	except OSError:
	    pass



######################

if __name__ == "__main__":
	reset_setting() 
	remove_conf_files()
	

	
	
