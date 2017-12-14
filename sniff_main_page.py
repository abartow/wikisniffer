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
	time.sleep(1)
	subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless", "--disable-gpu", url], close_fds=True)

def sniff_page(page_name):
	print "Sniffing {}".format(page_name)
	page_url = "https://en.wikipedia.org/wiki/{}".format(page_name)
	open_webbrowser_thread = threading.Thread(target=open_webbrowser_thread_target, args=(page_url,))
	open_webbrowser_thread.start()
	sniffer = WikipediaMetadataSniffer()
	sniffer.sniff(5)
	conversations = sniffer.extract_conversations()
	print "Sniffed: {}".format(conversations)
	return conversations

pageviews = WikipediaPageviewAnalyzer("pageviews-20171122-150000")

repeat_times = 5
num_pages_to_crawl = 1

'''
	pages_crawled = 0
	i = 24
	while pages_crawled < pages_to_crawl:
		page_title = pageviews.en_sorted[i][1]
		print page_title, i
		i += 1

		if page_title == "-" or page_title.startswith("Special:"):
			continue

		pages_crawled += 1
'''

output_dataset = []
for unused in range(repeat_times):
	metadata_mapping = {}

	pages_to_crawl = ["Darth_Vader", "Harvard_University"]

	for page_title in pages_to_crawl:
		conversations = sniff_page(page_title)
		if conversations == {}:
			# Retry once
			conversations = sniff_page(page_title)
		metadata_mapping[page_title] = conversations



	output_dataset.append(metadata_mapping)

print output_dataset

for page_title, connection_lengths in output_dataset[0].iteritems():
	for connection_endpoint in connection_lengths.keys():
		datapoints = []
		for i in range(repeat_times):
			datapoints.append(output_dataset[i][page_title].get(connection_endpoint, 0))

		print "{} {} {}".format(page_title, connection_endpoint, " ".join(map(str, datapoints)))