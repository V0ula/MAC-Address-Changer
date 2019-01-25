#!/usr/bin/env python

import subprocess
import optparse
import re

def return_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-n", "--network", dest="network", help="Network for which MAC address will be changed")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (input_value, arguments) = parser.parse_args()
    if not input_value.network:
        parser.error("[-] Input network or use --help to get more info")
    elif not input_value.new_mac:
        parser.error("[-] Input new MAC address or use --help to get more info")
    return input_value
    
def mac_address_change(network, new_mac):
    print("[+] Going to change MAC address for " + network + " into " + new_mac)
    subprocess.call(["ifconfig", network, "down"])
    subprocess.call(["ifconfig", network, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", network, "up"])
    
def get_existing_mac(network):
    network_info = subprocess.check_output(["ifconfig", network])
    existing_mac_address = re.search(r"([0-9a-f]{2}(?::[0-9a-f]{2}){5})", network_info)
    if existing_mac_address:
        return existing_mac_address.group(0)
    else:
        print("[-] Could not get the MAC address for the network")

input_value = return_arguments()

existing_mac = get_existing_mac(input_value.network)
print("Current MAC is " + str(existing_mac))

mac_address_change(input_value.network, input_value.new_mac)

existing_mac = get_existing_mac(input_value.network)
if existing_mac == input_value.new_mac:
    print("[+] MAC address was changed successfully into " + existing_mac)
else:
    print("[-] MAC address was not able to be changed.")

