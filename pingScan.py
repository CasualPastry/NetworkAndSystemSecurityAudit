###################################################################
#
# pingScan - performs a ping sweep of a given IP address space and
#            shows hosts that are up
#
###################################################################
import os, ipaddress, sys

def ping(IPAddr):
	if (os.system("ping -c 1 " + str(IPAddr) + " -W 1 > /dev/null")) == 0:
		print(str(IPAddr)+" - host is UP.\n")

def main():
	IPAddrRange = input("Please enter an IP address range: ")
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
	else:
		print("Provide input in the format 10.0.0.1-10.0.0.100 or 10.0.0.1/24")
		sys.exit()

		maxIP = ipaddress.ip_address(minIP) + inc

	while (ipaddress.ip_address(minIP) != ipaddress.ip_address(maxIP)):
		ping(minIP)
		minIP = ipaddress.ip_address(minIP) + 1

if __name__ == '__main__':
	main()