#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from lxml import etree

import dlbs
OPTIONS = dlbs.OPTIONS
FILENAME = dlbs.FILENAME

_HTML_HEADER = '''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<title>Ergebnisse von besser-studieren.nrw.de</title>
<style type="text/css">
.voteCount {padding-left: 2.5em;}
</style>
</head>
<body>
<h1>Ergebnisse von besser-studieren.nrw.de</h1>
'''

_HTML_FOOTER = '''</body>
</html>'''

def _meanDisagree(votes):
	votes = list(votes)
	return (sum(
		(
			abs(sum(OPTIONS[o]['weight'] * voteCount for o,voteCount in v.items()))
		/
			sum(v.values())
		)
		
		for v in votes)
	/ len(votes))


def main():
	with open(FILENAME, 'rb') as jsonf:
		res = json.load(jsonf)

	table = etree.Element('table')
	thead = etree.fromstring('<thead><tr><th>Titel</th><th>Autor</th></tr></thead>')
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

	for url,r in sorted(res.items()):
		tr = etree.Element('tr')
		tbody.append(tr)

		a = etree.Element('a')
		a.attrib['href'] = r['url']
		a.text = r['title']
		td = etree.Element('td')
		td.append(a)
		tr.append(td)

		td = etree.Element('td')
		td.text = r['author']
		tr.append(td)

		votes = r['votes']
		for o in sorted(OPTIONS):
			td = etree.Element('td')
			td.text = str(votes[o])
			tr.append(td)

		voteCount = sum(votes.values())
		td = etree.Element('td')
		td.attrib['class'] = 'voteCount'
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

	p = etree.Element('p')
	total.append(p)
	num = len(res)
	p.text = 'Anzahl Thesen: ' + str(num)

	p = etree.Element('p')
	total.append(p)
	voteCount = sum(sum(r['votes'].values()) for r in res.values())
	p.text = 'Anzahl Stimmen: ' + str(voteCount)

	p = etree.Element('p')
	total.append(p)
	meanDisagree = _meanDisagree(r['votes'] for r in res.values())
	meanDisagreeImportant = _meanDisagree(r['votes'] for r in res.values() if sum(r['votes'].values()) > 20)
	p.text = 'Durchschnittliche Diskussionsweite: %.2f (> 20 Stimmen: %.2f)' % (meanDisagree, meanDisagreeImportant)


	print(_HTML_HEADER)
	print(etree.tostring(table, pretty_print=True))
	print(etree.tostring(total, pretty_print=True))
	print(_HTML_FOOTER)


if __name__ == '__main__':
	main()
