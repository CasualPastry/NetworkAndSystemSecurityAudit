###################################################################
#
# arpEnum - performs a ping sweep of a given IP address space,
#           and maps MAC addresses to IP addresses that are up
#
###################################################################
import os, ipaddress, sys, logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import srp,Ether,ARP,conf

def scan(IPAddr, interface):
	if (os.system("ping -c 1 " + str(IPAddr) + " -W 1 > /dev/null")) == 0:
		conf.verb = 0
		ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = str(IPAddr)), timeout=2,
		iface = interface, inter=0.1)
		for send,rcv in ans:
			print(rcv.sprintf(r"%ARP.psrc% - %Ether.src%"))

def main():
	IPAddrRange = input("Please enter an IP address range: ")
	interface = input("Please enter the interface to scan from: ")
	opt1 = IPAddrRange.split("-")
	opt2 = IPAddrRange.split("/")

	if len(opt1) == 2:
		minIP = opt1[0]
		maxIP = opt1[1]
	elif len(opt2) == 2:
		minIP = opt2[0]
		cidr = opt2[1]
		if int(cidr) == 8:
			inc = 16777216 
		elif int(cidr) == 16:
			inc = 65026
		elif int(cidr) == 24:
			inc = 256
		maxIP = ipaddress.ip_address(minIP) + inc
	else:
		print("Provide input in the format 10.0.0.1-10.0.0.100 or 10.0.0.1/24")
		sys.exit()

	while (ipaddress.ip_address(minIP) != ipaddress.ip_address(maxIP)):
		scan(minIP, interface)
		minIP = ipaddress.ip_address(minIP) + 1

if __name__ == '__main__':
	main()