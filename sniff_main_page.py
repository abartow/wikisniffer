import webbrowser
import threading
from sniff_metadata import WikipediaMetadataSniffer
import time
from process_pageviews import WikipediaPageviewAnalyzer
import subprocess
import string
import random

# Make sure to call
# defaults write com.google.Chrome DiskCacheDir -string /dev/null
# before using this script to disable Chrome's cache.

def open_webbrowser_thread_target(url):
	subprocess.Popen(["osascript", "-e", 'quit app "Google Chrome"'], close_fds=True)
	time.sleep(3)
	subprocess.Popen(["open", "-a", "Google Chrome", url], close_fds=True)

def sniff_page(page_name):
	page_url = "https://en.wikipedia.org/wiki/{}".format(page_name)
	open_webbrowser_thread = threading.Thread(target=open_webbrowser_thread_target, args=(page_url,))
	open_webbrowser_thread.start()
	sniffer = WikipediaMetadataSniffer()
	sniffer.sniff(15)
	return sniffer.extract_conversations()

pageviews = WikipediaPageviewAnalyzer("pageviews-20171031-110000")

repeat_times = 5
pages_to_crawl = 1

output_dataset = []
for unused in range(repeat_times):
	metadata_mapping = {}

	pages_crawled = 0
	i = 24
	while pages_crawled < pages_to_crawl:
		page_title = pageviews.en_sorted[i][1]
		print page_title, i
		i += 1

		if page_title == "-" or page_title.startswith("Special:"):
			continue

		conversations = sniff_page(page_title)
		if conversations == {}:
			# Retry once
			conversations = sniff_page(page_title)
		metadata_mapping[page_title] = conversations

		pages_crawled += 1

	output_dataset.append(metadata_mapping)

print output_dataset

for page_title, connection_lengths in output_dataset[0].iteritems():
	for connection_endpoint in connection_lengths.keys():
		datapoints = []
		for i in range(repeat_times):
			datapoints.append(output_dataset[i][page_title].get(connection_endpoint, 0))

		print "{} {} {}".format(page_title, connection_endpoint, " ".join(map(str, datapoints)))