#!/usr/bin/env python

import contextlib
from lxml import etree
import json
import sys
try:
	import urllib3 as urllib
except ImportError:
	import urllib

OPTIONS = {
	'1': {
		'string': '--',
		'weight': -1,
	},
	'2': {
		'string': '-',
		'weight': -0.5,
	},
	'3': {
		'string': '0',
		'weight': 0,
	},
	'4': {
		'string': '+',
		'weight': 0.5,
	},
	'5': {
		'string': '++',
		'weight': 1,
	}
}
FILENAME = 'bs-result.json'

def analyze(url):
	with contextlib.closing(urllib.urlopen(url)) as urlf:
		url = urlf.geturl()
		content = urlf.read()
	doc = etree.HTML(content)

	title = doc.find('.//h1[@class="title"]').text
	votes = {}
	for o in OPTIONS:
		votes[o] = int(doc.find('.//div[@class="votingresults"]/div[@class="option-' + o + '"]').text.strip('()'))
	voteCount = sum(votes.values())
	decision = sum(OPTIONS[o]['weight'] * votes for o,votes in votes.items())
	nextUrl = 'http://besser-studieren.nrw.de' + doc.find('.//a[@class="navigate_next"]').attrib['href']
	authorNode = doc.find('.//div[@class="username"]')
	aNode = authorNode.find('./a')
	if aNode is not None:
		author = aNode.text
	else:
		author = authorNode.text
	if author.startswith('verfasst von: '):
		author = author[len('verfasst von: '):]
	author = author.strip()

	return {
		'author': author,
		'url': url,
		'title': title,
		'votes': votes,
		'nextUrl': nextUrl,
	}

def main():
	urls = {}

	url = 'http://besser-studieren.nrw.de/node/676/0'
	while True:
		r = analyze(url)
		url = r['url']
		if url in urls:
			break
		urls[url] = r
		print(url)
		url = r['nextUrl']

	with open(FILENAME, 'wb') as jsonf:
		json.dump(urls, jsonf)

if __name__ == '__main__':
	main()
