# A simple recorder which saves the records into a SQLite3 database with
# a matching timestamp of when the keystroke was recorded".

import sqlite3

class SQLiteRecorder:
    def __init__(self):
        self.conn = sqlite3.connect("pykeystat.db")

        c = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='keystrokes';")

        if c.fetchone() is None:
            self.conn.execute("CREATE TABLE keystrokes (key, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

    def record(self, keystroke):
        c = self.conn.execute("INSERT INTO keystrokes (key) values (?)", 
                              (keystroke,))
        self.conn.commit()
