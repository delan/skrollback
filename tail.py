#!/usr/bin/env python

import sys
import skypelib
import config

if len(sys.argv) != 2:
	print 'Usage:', sys.argv[0], 'chat.conv_dbid'
	sys.exit()

def echo(*args):
	out = u''
	for u in args:
		out += u
	print out.encode('utf-8')

def on_message(row):
	if row[17] is None:
		return
	echo('[', unicode(row[9]), ' ', unicode(row[4]), '] ', row[17])

skypelib.monitor.monitor(config.main_db_path, int(sys.argv[1]), on_message)
