#!/usr/bin/env python

import os
import sys
import time
import shutil
import tempfile
import sqlite3
import watchdog.events
import watchdog.observers
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

class MainDatabaseEventHandler(watchdog.events.FileSystemEventHandler):
	def __init__(self, convo):
		self.convo = convo
		self.last_message_id = 0
		self.internal_print_tail()
	def on_modified(self, event):
		if event.src_path != config.main_db_path:
			return
		self.internal_print_tail()
	def internal_print_tail(self):
		f = tempfile.mkstemp()[1]
		shutil.copyfile(config.main_db_path, f)
		c = sqlite3.connect(f)
		for r in c.execute(
			'SELECT id, timestamp, author, body_xml\
			FROM Messages WHERE convo_id = ? AND id > ?\
			ORDER BY id', (self.convo, self.last_message_id)):
			echo('[', r[1], ' ', r[2], '] ', r[3])
			self.last_message_id = r[0]
		c.close()
		os.remove(f)

observer = watchdog.observers.Observer()
observer.schedule(
	MainDatabaseEventHandler(int(sys.argv[1])),
	os.path.dirname(config.main_db_path),
	recursive=True
)
observer.start()

try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	observer.stop()

observer.join()
