import argparse
from functools import reduce

# Analyzer that produces sorted list of english wikipedia pages by popularity.
class WikipediaPageviewAnalyzer():
	def __init__(self, path_to_pageview_file):
		with open(path_to_pageview_file, 'r') as pageview_file:
			raw_pageviews = pageview_file.read()
			# List of tuples (project, page_title, pageviews, unused)
    		self.pages_viewed = map(lambda page_viewed_raw: page_viewed_raw.split(" "), raw_pageviews.split("\n"))
    		self.en = filter(lambda x: x[0] == "en", self.pages_viewed)
    		self.en_sorted = sorted(self.en, key=lambda x: int(x[2]), reverse=True)
    		self.en_num_views = sum([int(x[2]) for x in self.en_sorted])



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process Wikipedia pageviews files.')
	parser.add_argument('file', metavar='NAME', help='path to pageviews file')
	args = parser.parse_args()

	pageview_file_path = args.file

	pageviews = WikipediaPageviewAnalyzer(pageview_file_path)

	accum_page_views = 0
	pages = 0
	for page_view in pageviews.en_sorted:
		accum_page_views += int(page_view[2])
		pages += 1
		if pages > 3000: break

	print len(pageviews.en_sorted)
	print pageviews.en_sorted[0]
	print pageviews.en_sorted[1]
	print pageviews.en_sorted[2]
	print "Total Pageviews: {}".format(pageviews.en_num_views)
	print "Top 3000: {} {}".format(accum_page_views, float(accum_page_views) / pageviews.en_num_views)