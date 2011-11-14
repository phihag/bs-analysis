#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from lxml import etree

import dlbs
OPTIONS = dlbs.OPTIONS

_HTML_HEADER = '''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<title>Ergebnisse von besser-studieren.nrw.de</title>
</head>
<body>
<h1>Ergebnisse von besser-studieren.nrw.de</h1>
'''

_HTML_FOOTER = '''</body>
</html>'''



def main():
	res = json.load(sys.stdin)

	table = etree.Element('table')
	thead = etree.fromstring('<thead><tr><th>Titel</th></tr></thead>')
	tr = thead.find('.//tr')
	table.append(thead)
	for o,od in sorted(OPTIONS.items()):
		th = etree.Element('th')
		th.text = od['string']
		tr.append(th)
	tr.append(etree.fromstring('<th>Stimmen</th>'))
	tr.append(etree.fromstring('<th>Ergebnis</th>'))
	tr.append(etree.fromstring('<th>⌀</th>'))
	tbody = etree.Element('tbody')
	table.append(tbody)

	for url,r in res.items():
		tr = etree.Element('tr')
		tbody.append(tr)

		a = etree.Element('a')
		a.attrib['href'] = r['url']
		a.text = r['title']
		td = etree.Element('td')
		td.append(a)
		tr.append(td)

		votes = r['votes']
		for o in sorted(OPTIONS):
			td = etree.Element('td')
			td.text = str(votes[o])
			tr.append(td)

		voteCount = sum(votes.values())
		td = etree.Element('td')
		td.text = str(voteCount)
		tr.append(td)

		decision = sum(OPTIONS[o]['weight'] * votes for o,votes in votes.items())
		td = etree.Element('td')
		td.text = str(decision)
		tr.append(td)

		mean = decision / voteCount
		td = etree.Element('td')
		td.text = '%.2f' % mean
		tr.append(td)

	total = etree.Element('div')
	votesTotal = etree.Element('p')
	total.append(votesTotal)
	voteCount = sum(sum(r['votes'].values()) for r in res.values())
	total.text = 'Anzahl Stimmen: ' + str(voteCount)

	print(_HTML_HEADER)
	print(etree.tostring(table, pretty_print=True))
	print(etree.tostring(total, pretty_print=True))
	print(_HTML_FOOTER)


if __name__ == '__main__':
	main()
