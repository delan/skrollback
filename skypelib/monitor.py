import os
import time
import shutil
import tempfile
import sqlite3
import watchdog.events
import watchdog.observers

class MainDatabaseEventHandler(watchdog.events.FileSystemEventHandler):
	def __init__(self, main_db_path, convo_id, message_callback):
		self.main_db_path = main_db_path
		self.convo_id = convo_id
		self.message_callback = message_callback
		self.last_message_id = 0
		self.handle_change()
	def on_modified(self, event):
		if event.src_path != self.main_db_path:
			return
		self.handle_change()
	def handle_change(self):
		f = tempfile.mkstemp()[1]
		shutil.copyfile(self.main_db_path, f)
		c = sqlite3.connect(f)
		for r in c.execute(
			'SELECT * FROM Messages WHERE convo_id = ? AND id > ?\
			ORDER BY id', (self.convo_id, self.last_message_id)):
			self.message_callback(r)
			self.last_message_id = r[0]
		c.close()
		os.remove(f)

def monitor(main_db_path, convo_id, message_callback):
	observer = watchdog.observers.Observer()
	observer.schedule(
		MainDatabaseEventHandler(
			main_db_path,
			convo_id,
			message_callback
		),
		os.path.dirname(main_db_path),
		recursive=True
	)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
