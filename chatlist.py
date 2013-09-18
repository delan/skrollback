#!/usr/bin/env python

import sqlite3
import config

c = sqlite3.connect(config.main_db_path)
for r in c.execute('SELECT conv_dbid, friendlyname FROM Chats\
	ORDER BY activity_timestamp'):
	print '[' + str(r[0]) + ']' , r[1].encode('utf-8')
c.close()
