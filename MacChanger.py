import subprocess
import optparse
import re

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-i","--interface",dest="interface",help="Interface to change its Mac address")
	parser.add_option("-m","--mac",dest="New_MacADR",help="New MAC address")
	
	(options, arguments) = parser.parse_args()

	if not options.interface:
		parser.error("[-] Please specify an interface, use --help for more infor.")
	elif not options.New_MacADR:
		parser.error("[-] Please specify an macadddress, use --help for more infor.")
	return options

def change_mac(interface, New_MacADR):
	print("Change Mac " +interface+ " to " +New_MacADR)

	subprocess.call("ifconfig "+interface+" down", shell = True)
	subprocess.call("ifconfig "+interface+" hw ether " + New_MacADR, shell = True)
	subprocess.call("ifconfig "+interface+" up", shell = True)

# parser = optparse.OptionParser()
# parser.add_option("-i","--interface",dest="interface",help="Interface to change its Mac address")
# parser.add_option("-m","--mac",dest="New_MacADR",help="New MAC address")

def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result.decode('utf-8') )
	if mac_address_search_result:
		print(mac_address_search_result.group(0))
	else:
		print("[-] Could not read Mac address." )

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.New_MacADR)

current_mac = get_current_mac(options.interface)
if current_mac == options.New_MacADR:
	print("[+] MAC address was successfilly changed to " + current_mac)
else:
	print("[+] MAC address did not get changed.")

# interface = options.interface
# New_MacADR = options.New_MacADR
# print("Change Mac " +interface+ " to " +New_MacADR)
# subprocess.call("ifconfig "+interface+" down", shell = True)
# subprocess.call("ifconfig "+interface+" hw ether " + New_MacADR, shell = True)
# subprocess.call("ifconfig "+interface+" up", shell = True)

# change_mac(options.interface, options.New_MacADR)
# subprocess.call("ifconfig", shell = True)