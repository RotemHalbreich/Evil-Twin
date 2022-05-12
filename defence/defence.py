from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt 
import os
import time


ap_list = []
### Coloum indices for 'ap_list'. 
ESSID = 0
BSSID = 1
CHANNEL = 2
essids_set = set()

### Console colors
W  = '\033[0m'  # white 
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan


##############################################
############### Interface Mode ###############
##############################################

"""
In this function the user choose the interface that will scan the network and switch it to monitor mode.
"""
def monitor_mode():
    global interface
    print(G + "*** Step 1:  Choosing an interface to put in 'monitor mode'. *** \n")
    empty = input ("Press Enter to continue.........\n")
    print(W)
    os.system('ifconfig')
    interface = input(G + "Please enter the interface name you want to put in 'monitor mode': ")
    print(W)
    # Put the choosen interface in 'monitor mode'
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode monitor')
    os.system('ifconfig ' + interface + ' up')
    # os.system('iwconfig') #check

"""
In this function the responsible for switch back to managed mode
"""
def managed_mode():
    print(G + "\n*** Step 4: Put the interface back in 'managed mode'. *** \n")
    empty = input ("Press Enter in order to put " + interface + " in 'managed mode' .........\n")
    print(W)
    # Put the choosen interface back in 'managed mode'
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode managed')
    os.system('ifconfig ' + interface + ' up')
    print(B + "[**] - The interface: " + interface + ", is now in Managed Mode. \nYou can check it here : \n")
    os.system('iwconfig')



##############################################
############### APs Scanning #################
##############################################

"""
In this function the responsible for Scanning the network for AP
""" 
def ap_scan_rap():
    print(G + "*** Step 2: Scanning the network for AP to attack. *** \n")
    empty = input ("Press Enter to continue.........")
    # os.system ('airodump-ng ' + interface)
    ap_scan()

"""
In this function the responsible for present to the user all the APs that were found, and he choose which AP he want to attack. 
"""
def ap_scan():
    global search_timeout
    search_timeout = int(input(G + "Please enter the scanning time frame in seconds: "))
    channel_changer = Thread(target = change_channel)
    # A daemon thread runs without blocking the main program from exiting
    channel_changer.daemon = True
    channel_changer.start()
    print("\n Scanning for networks...\n")
    # Sniffing packets - scanning the network for AP in the area
    # iface – the interface that is in monitor mode
    # prn – function to apply to each packet
    # timeout – stop sniffing after a given time
    sniff(iface = interface, prn = ap_scan_pkt, timeout=search_timeout)
    num_of_ap = len(ap_list)
    if num_of_ap > 0: 
        # If at least 1 AP was found. 
        print("\n*************** APs Table ***************\n")
        for x in range(num_of_ap):
            print("[" + str(x) + "] - BSSID: " + ap_list[x][BSSID] + " \t Channel:" + str(ap_list[x][CHANNEL]) + " \t AP name: " + ap_list[x][ESSID]) 
        print("\n************* FINISH SCANNING *************\n")
	# Choosing the AP to defence
        ap_index = int(input("Please enter the number of the AP you want to defence: "))
	# Print the choosen AP
        print("You choose the AP: [" + str(ap_index) + "] - BSSID: " + ap_list[ap_index][BSSID] + " Channel:" + str(ap_list[ap_index][CHANNEL]) + " AP name: " + ap_list[ap_index][ESSID])
        # set_channel(int(ap_list[ap_index][CHANNEL]))
        global ap_mac
        global ap_name
        global ap_channel
        ap_mac = ap_list[ap_index][BSSID]
        ap_name = ap_list[ap_index][ESSID]
        ap_channel = ap_list[ap_index][CHANNEL]
    else: 
        # If no AP was found. 
        rescan = input("No networks were found. Do you want to rescan? [Y/n] ")
        if rescan == "n":
            print("  Sorry :(  ")
            managed_mode()
            sys.exit(0)
        else:
            ap_scan()


"""
This function is resposible for check in each channel in the range [1,14]. 
""" 
def change_channel():
    channel_switch = 1
    while True:
        os.system('iwconfig %s channel %d' % (interface, channel_switch))
        # switch channel in range [1,14] each 0.5 seconds
        channel_switch = channel_switch % 14 + 1
        time.sleep(0.5)

'''
### After the user choose the AP he want to attack, we want to set the interface's channel to the same channel as the choosen AP. 
def set_channel(channel):
    os.system('iwconfig %s channel %d' % (interface, channel))
'''


### sniff(..., prn = ap_scan_pkt, ...) 
### The argument 'prn' allows us to pass a function that executes with each packet sniffed. 
def ap_scan_pkt(pkt):
    if pkt.haslayer(Dot11Beacon):
        # Get the BSSID (MAC ADDR) of the AP
        bssid = pkt[Dot11].addr2
        # Get the ESSID (name) of the AP
        essid = pkt[Dot11Elt].info.decode()
        if essid not in essids_set:
            essids_set.add(essid)
            stats = pkt[Dot11Beacon].network_stats()
            # Get the channel of the AP
            channel = stats.get("channel")
            ap_list.append([essid, bssid, channel])
            # print("AP name: %s,\t BSSID: %s,\t Channel: %d." % (essid, bssid, channel))




##############################################
########## Deauthentication Defence ##########
##############################################
"""
This function we will sniff packets and search for deauthentication packets and will alert that there is deathentication attack on the choosen AP
"""
def deathentication_check():
	print(G + "*** Step 3: Sniffing the packets and checking for deauthentication attack. *** \n")
	print(G + "In case that will be sniffed 30 deauthentication packets, you will alerted that there is attempt to do deathentication attack to the AP you choose. \n")
	empty = input ("Press Enter to continue.........\n")
	print(B + "Sniffing packets for 60 second ...")
	print(W)
	# Sniffing packets - searching for deauthentication packets that are sending to the choosen AP 
	sniff(iface=interface, prn = packet_handler , stop_filter=stopfilter)
	# sniff(iface="wlxc83a35c2e0b7", prn = PacketHandler , stop_filter=stopfilter)
	print(W)


### sniff(..., prn = packet_handler, ...) 
### The argument 'prn' allows us to pass a function that executes with each packet sniffed. 
count = 0
def packet_handler(pkt):
	global count
	global start_time
	# If we capture deauthentication packet
	# Deauthentication frame is management frame (type 0) and subtype 12 (0xC) 
	# Management frames are used by IEEE 802.11 to permit a wireless client to negotiate with a Wireless Access Point 
	if pkt.type == 0 and pkt.subtype == 0xC:
		try:
			# If we capture deauthentication packet that intended to the choosen AP
			if ap_mac in str(pkt.addr2):
				count=count+1
				print (O + "Deauthentication packet has been sniffed. Packet number: " + str(count))
		except:
			print("An exception occurred")
	# If 60 sec had passed and deauthentication attack didn't occur, than we reset count to 0 and start counting again
	if  time.time()-start_time > 60 :
		count=0		
		print(W + "Meanwhile, everything is OK :) ")
		start_time=time.time()

"""
THis function is resposible for stop condition for sniffing the deauthentication packets
"""
def stopfilter(x):
	# If there was attemp to do deathentication attack, we stop the packets sniffing and alerts the user about it
	if count==30:
		print(R + "WARNNING!! There is attemp to do deathentication attack on your netwotk. \n")
		return True
	else:
		return False



if __name__ == "__main__":

	if os.geteuid():
		sys.exit(R + '[**] Please run as root')
    
	print(B + "********************************************************************** \n")
	print("************ Part 2: defence from deauthentication attack ************ \n")
	print("********************************************************************** \n")
	
	### Step 1:  Choosing an interface to put in 'monitor mode'.
	monitor_mode()
	
	### Step 2: Choosing the AP that we want to attack. 
	ap_scan_rap()
	
	### Step 3: Sniffing the packets and checking for deauthentication attack.
	start_time = time.time()
	deathentication_check()	
	
	### Step 4: Put the interface back in 'managed mode'.
	managed_mode()
	
	
