#!/usr/bin/env python

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
	json.load(sys.stdin)

	table = etree.Element('table')
	thead = etree.fromstring('<thead><tr><th>Titel</th></tr></thead>')
	tr = thead.find('.//tr')
	table.append(thead)
	for o,od in sorted(OPTIONS.items()):
		th = etree.Element('th')
		th.text = od['string']
		tr.append(th)
	tr.append(etree.fromstring('<th>Anzahl Stimmen</th>'))
	tr.append(etree.fromstring('<th>Ergebnis</th>'))
	tbody = etree.Element('tbody')
	table.append(tbody)
		urls.add(r['url'])
		tr = etree.Element('tr')
		tbody.append(tr)

		a = etree.Element('a')
		a.attrib['href'] = r['url']
		a.text = r['title']
		td = etree.Element('td')
		td.append(a)
		tr.append(td)

		for o in sorted(OPTIONS):
			td = etree.Element('td')
			td.text = str(r['votes'][o])
			tr.append(td)

		td = etree.Element('td')
		td.text = str(r['voteCount'])
		tr.append(td)

		td = etree.Element('td')
		td.text = str(r['decision'])
		tr.append(td)

		nextUrl = r['nextUrl']

	print(_HTML_HEADER)
	print(etree.tostring(table, pretty_print=True))
	print(_HTML_FOOTER)


if __name__ == '__main__':
	main()
