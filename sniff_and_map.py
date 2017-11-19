from sniff_metadata import WikipediaMetadataSniffer

mapping = {}
with open("mapping", 'r') as mapping_file:
	mapping_data = mapping_file.read()
	mapping_datapoints = map(lambda x: x.split("	"), mapping_data.split("\n"))
	for title, endpoint, datapoint, std_dev in mapping_datapoints:
		if title not in mapping:
			mapping[title] = {endpoint: (float(datapoint), float(std_dev))}
		else:
			mapping[title][endpoint] = (float(datapoint), float(std_dev))

print "Sniffing for Wikipedia Traffic..."

sniffer = WikipediaMetadataSniffer()
sniffer.sniff(20)
conversation = sniffer.extract_conversations()

print "Extracted Metadata!"

distances = []
for title, connection_lengths in mapping.iteritems():
	distance = 0
	for endpoint in connection_lengths.keys():
		connection_length, std_dev = connection_lengths[endpoint]
		distance += ((connection_length - conversation[endpoint]) / std_dev)**2

	distance = distance**0.5

	distances.append((title, distance))

distances = sorted(distances, key=lambda x: x[1])

print "I think you visited the article for {} (distance={})".format(distances[0][0], distances[0][1])