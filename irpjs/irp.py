#!/usr/bin/python3

# server for js impress remote

import json
from collections import OrderedDict
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource


def send_all (msg):
    for ws in clients:
        ws.send(msg)

clients = []

class IRPApp (WebSocketApplication):
    def __init__(self, parent):
        super(WebSocketApplication, self).__init__()
        self.parent = parent
        self.lo_slideshow_contr = self.parent.lo_slideshow_contr

    def on_open (self):
        global clients
        clients.append(self.ws)
        self.connected = False

        print("new conn")

    def on_message (self, message):

        # handshake
        if '\"hello\"' == message:
            self.ws.send('hello')
            self.connected = True
            self.lo_slideshow_contr.send_slide_info()   # TODO check if this works
            print('recv handshake')

        # disconnected
        elif None == message:
            # TODO do something?
            pass

        else:
            data = json.loads(message)
            self.irp_msg(data)

    def irp_msg (self, msg):
        action = msg["action"]

        # TODO add exceptions for msg["xxxx"] in case there's no such key

        # NOTE it could be imagined that we'd want to process/ make checks
        #      before calling the UNOClient methods
        if 'transition_next' == action:
            self.lo_slideshow_contr.go_to_next_Slide()

        elif 'transition_previous' == action:
            self.lo_slideshow_contr.go_to_previous_Slide()

        elif 'goto_slide' == action:
            number = msg["number"]
            self.lo_slideshow_contr.goto_slide(number)

        elif 'presentation_start' == action:
            self.parent.start_presentation()

        elif 'presentation_stop' == action:
            self.parent.end_curent_presentation()

        # TODO add this function presentation_blank_screen
        elif 'presentation_blank_screen' == action:
            pass

        elif 'presentation_resume' == action:
            self.lo_slideshow_contr.resume_presentation()

    def on_close (self, reason):
        global clients
        clients.remove(self.ws)

        print("close", reason)

def run_irp_server(parent, address = '0.0.0.0', port = 5100):
    addr = (address, port)
    WebSocketServer(addr, Resource(OrderedDict([('/', IRPApp(parent))]))).serve_forever()

