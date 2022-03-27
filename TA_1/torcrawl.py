#!/usr/bin/python

import socket
import socks
import argparse

# TorCrawl Modules
from modules.crawler import crawler
from modules.checker import *

help = '''
General:
-h, --help         : Help
-v, --verbose      : Show more informations about the progress
-u, --url *.onion  : URL of Webpage to crawl or extract

Crawl:
-d, --cdepth      : Set depth of crawl's travel (Default: 1)
'''


# Set socket and connection with TOR network
def connecttor():
	try:
		port = 9050
		# Set socks proxy and wrap the urllib module
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', port)
		socket.socket = socks.socksocket

		# Perform DNS resolution through the socket
		def getaddrinfo(*args):
			return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

		socket.getaddrinfo = getaddrinfo
	except:
		e = sys.exc_info()[0]
		print(("Error: %s" % e + "\n## Can't establish connection with TOR"))


def main():
	# Initialize necessary variables
	cdepth = 1

	parser = argparse.ArgumentParser(
		description="TorCrawl.py is a python script to crawl and extract (regular or onion) webpages through TOR network.")

	# General
	parser.add_argument(
		'-v',
		'--verbose',
		action='store_true',
		help='Show more information about the progress'
	)
	parser.add_argument(
		'-u',
		'--url',
		help='URL of webpage to crawl or extract'
	)

	# Crawl
	parser.add_argument(
		'-d',
		'--cdepth',
		help='Set depth of crawl\'s travel (Default: 1)'
	)

	args = parser.parse_args()

	# Parse arguments to variables
	if args.cdepth:
		cdepth = args.cdepth

	# Connect to TOR
		checktor(args.verbose)
		connecttor()

	if args.verbose:
		checkip()
		print(('## URL: ' + args.url))

	# Canon/ion of website and create path for output
	if len(args.url) > 0:
		global website
		global outpath
		website = urlcanon(args.url, args.verbose)
		outpath = folder(extract_domain(website), args.verbose)


		lst = crawler(website, cdepth, outpath, args.verbose)
		lstfile = open(outpath + '/links.txt', 'w+')
		for item in lst:
			lstfile.write("%s\n" % item)
		lstfile.close()
		print(("## File created on " + os.getcwd() + "/" + outpath + "/links.txt"))


if __name__ == "__main__":
    main()
