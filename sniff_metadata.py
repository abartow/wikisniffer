import pyshark
import socket
import logging
from sets import Set

# Attempts to resolve ip to its hostname. If ip cannot be resolved, returns ip.
def resolve_ip(ip):
	try:
		hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
		return hostname
	except socket.herror:
	     return ip

# The first layer of a packet is the IP layer. We use this in place of "ip" because packets can be IPv4 or IPv6
IP_LAYER = 1

class WikipediaMetadataSniffer():
	def __init__(self):
		self.captured_packets = []

	def sniff(self, timeout):
		capture = pyshark.LiveCapture(interface='en0')
		capture.sniff(timeout=timeout)
		self.captured_packets = captured_packets = capture[0:len(capture)-1]
		capture.close()
		del capture


	def extract_conversations(self):
		tcp_packets = filter(lambda packet: 'tcp' in packet, self.captured_packets)
		#seen_hosts = {}
		#for packet in tcp_packets:
		#	seen_hosts[resolve_ip(packet[IP_LAYER].src)] = True
		#print seen_hosts.keys()

		wiki_filter = lambda packet: resolve_ip(packet[IP_LAYER].src).endswith("wikimedia.org")
		wiki_packets = filter(wiki_filter, tcp_packets)

		conversations = {}
		seen_packets = Set()
		for packet in wiki_packets:
			packet_signature = (packet['ip'].src, packet['tcp'].srcport, packet['ip'].dst, packet['tcp'].dstport, packet['tcp'].stream, packet['tcp'].seq)
			
			if packet_signature in seen_packets:
				continue
			else:
				seen_packets.add(packet_signature)

			if resolve_ip(packet[IP_LAYER].src) in conversations:
				conversations[resolve_ip(packet[IP_LAYER].src)] += int(packet["tcp"].len)
			else:
				conversations[resolve_ip(packet[IP_LAYER].src)] = int(packet["tcp"].len)

		return conversations

if __name__ == "__main__":
	wiki_sniffer = WikipediaMetadataSniffer()
	wiki_sniffer.sniff(10)
	print wiki_sniffer.extract_conversations()