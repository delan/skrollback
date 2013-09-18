#!/usr/bin/env python

import sys
import skypelib
import config
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
	print 'Usage:', sys.argv[0], 'chat.conv_dbid'
	sys.exit()

def echo(*args):
	out = u''
	for u in args:
		out += u
	print out.encode('utf-8')

def xmlsan(u):
	import re
	return re.sub(
		u'[\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff]',
		'', u
	)

def on_message(row):
	if row[17] is None:
		return
	m = ET.fromstring(
		(u'<SkypeMessage>' +
		xmlsan(row[17]) +
		u'</SkypeMessage>').encode('utf-8')
	)
	m.set('timestamp', str(row[9]))
	m.set('author', row[4])
	echo(ET.tostring(m, encoding='utf-8').decode('utf-8'))

skypelib.monitor.monitor(config.main_db_path, int(sys.argv[1]), on_message)
