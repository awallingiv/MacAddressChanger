#!/usr/bin/env python
import subprocess
import optparse
import re


# must be run with arguments!
# example: python main.py -i eth0 -m 00:11:22:33:44:55
"""
-----****** get_Arguments ******-----
function will create a parser object,
add two options to it, and return it.
input: 
"""
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC of")
    parser.add_option("-m", "--mac", dest="new_mac", help="new mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Invalid interface, double-check and try again.  --help for help")
    elif not options.new_mac:
        parser.error("Invalid mac address format, double-check and try again.  --help for help")
    return options

"""
-----****** change_mac ******-----
This function will call the necessary
subprocesses needed to change the mac 
address(down, change, up)
"""
def change_mac(interface, new_mac):
    print("Changing Mac address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

"""
-----****** getCurrentMac ******-----
function will gather data from an ifconfig
call, find the mac address using REGEX, and then
return that MAC address (if successful)
"""
def getCurrentMac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    regexMac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result) #format of MAC address

    if regexMac:
        return regexMac.group(0)
    else:
        print("Could not read MAC address ")


options = get_arguments()

currentMac = getCurrentMac(options.interface)
print("Current MAC address: " + str(currentMac))

change_mac(options.interface, options.new_mac)

currentMac = getCurrentMac(options.interface)
if currentMac == options.new_mac:
    print("MAC address successfully changed to " + currentMac)
else:
    print("MAC address change failed.")
