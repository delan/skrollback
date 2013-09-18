#!/usr/bin/env python

import sys
import skypelib
import config

if len(sys.argv) != 2:
	print 'Usage:', sys.argv[0], 'chat.conv_dbid'
	sys.exit()

def echo(*args):
	out = ''
	for i in range(len(args) - 1):
		out += unicode(args[i]).encode('utf-8')
	out += unicode(args[len(args) - 1]).encode('utf-8')
	print out

def on_message(row):
	echo('[', row[9], ' ', row[4], '] ', row[17])

skypelib.monitor.monitor(config.main_db_path, int(sys.argv[1]), on_message)
