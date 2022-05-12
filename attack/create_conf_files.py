import os
import sys


##############################################
######## hostapd configuration file ##########
##############################################
'''
hostapd (host access point daemon) is a user space daemon software 
enabling a network interface card to act as an access point and authentication server
'''
 
# Set the interface that will be used as the fake AP.
line1="interface="+ sys.argv[1] + "\n"
# Set the name of the fake AP. 
line2="ssid=" + sys.argv[2] + "\n"
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


##############################################
######## dnsmasq configuration file ##########
##############################################
'''
dnsmasq is free software intended for small computer networks
dnsmasq is providing: 
Domain Name System (DNS) caching, 
a Dynamic Host Configuration Protocol (DHCP) server, 
router advertisement, and network boot features,
'''

# Set the interface that will be  used as the fake AP.
line1="interface="+sys.argv[1]+"\n"
# Set the range of the IP address allocations, and the time limit for each allocation.
line2="dhcp-range=10.0.0.10,10.0.0.100,8h\n"
# Set the gateway address of the fake AP (3 stand for gateway address).
line3="dhcp-option=3,10.0.0.1\n"
# Set the DNS server address of the fake AP (6 stand for DNS server address).
line4="dhcp-option=6,10.0.0.1\n"
# Set the IP address of the fake AP. All queries will be sent to this address.
line5="address=/#/10.0.0.1\n"

### If this file is exists, we delete it.
try:
    os.remove("./dnsmasq.conf")
except OSError:
    pass
### Create and write the dnsmasq configuration file.
dnsmasq_file=open("./dnsmasq.conf", "a+")
dnsmasq_file.write(line1)
dnsmasq_file.write(line2)
dnsmasq_file.write(line3)
dnsmasq_file.write(line4)
dnsmasq_file.write(line5)
