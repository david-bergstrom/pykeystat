from keylistener import KeyListener
from sqliterecorder import SQLiteRecorder 

listener = KeyListener()
recorder = SQLiteRecorder()
listener.set_recorder(lambda x : recorder.record(x))
listener.setup()

i = ""
while i != "stop":
    i = raw_input()
