import scapy.all as scapy
import optparse

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-t","--targte",dest="target",help="Target IP / IP range.")
	(options, arguments) = parser.parse_args()
	if not options.target:
		parser.error("[-] Please specify an interface, use --help for more infor.")
	return options


def scan(ip):
	arp_request = scapy.ARP(pdst=ip)
	# arp_request.show()
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	# broadcast.show()
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

	clients_list = []
	for element in answered_list:
		clients_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
		clients_list.append(clients_dict)
	return clients_list

def print_result(return_list):
	print("IP\t\t\tMac Address")
	for client in return_list:
		print(client["ip"] + "\t\t" + client["mac"])
	


	# answered,unanswered = scapy.srp(arp_request_broadcast,timeout=1)
	# print(answered.summary())
	# arp_request_broadcast.show()
	# scapy.ls(scapy.Ether())
	# print(arp_request.summary())
	# scapy.ls(scapy.ARP())
options = get_arguments
scan_result = scan("10.0.2.1/24")
print_result(scan_result)