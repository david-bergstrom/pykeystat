# A simple class which uses Xlib to listen to any key event made in
# X. The class can use a custom recorder which is used to record any
# event. The record function takes a single input and is called
# whenever a new input is recorded.

from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq
from Xlib import XK

class KeyListener:
    def __init__(self):
        self.disp = None
        self.root = None
        self.record = None

    def setup(self):
        # get current display
        self.disp = Display()
        self.root = self.disp.screen().root

        # Monitor keypress and button press
        ctx = self.disp.record_create_context(
            0,
            [record.AllClients],
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }])
        self.disp.record_enable_context(ctx, self.handler)
        self.disp.record_free_context(ctx)

    def handler(self, reply):
        """ Self function is called when a xlib event is fired """
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data,
                                                                 self.disp.display,
                                                                 None, None)

            if event.type == X.KeyPress:
                if event.detail == 36:
                    self.record("enter")
                elif event.detail == 22:
                    self.record("backspace")
                elif event.detail == 37:
                    self.record("control")
                elif event.detail == 64:
                    self.record("alt")
                elif event.detail == 108:
                    self.record("alt-gr")
                        
                key = XK.keysym_to_string(
                    self.disp.keycode_to_keysym(event.detail, event.state))

                if key:
                    self.record(key)
                    
    def key_listen_loop(self):
        while True:
            self.root.display.next_event()
            
    def set_recorder(self, r):
        self.record = r


if __name__ == "__main__":
    def printer(x):
        print x
    listener = KeyListener()
    listener.set_recorder(printer)
    listener.setup()
    i = ""
    while i != "stop":
        i = raw_input()
