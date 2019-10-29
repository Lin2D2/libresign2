#!/usr/bin/python3

# server for js impress remote

import json
from collections import OrderedDict
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource


def send_all (msg):
    for ws in clients:
        ws.send(msg)

clients = []

parent = None
lo_slideshow_contr = None

class IRPApp (WebSocketApplication):
    def on_open (self):
        global clients
        clients.append(self.ws)
        lo_slideshow_contr.send_slide_info()
        self.connected = False

        print("new conn")

    def on_message (self, message):

        # handshake
        if '\"hello\"' == message:
            self.ws.send('hello')
            self.connected = True
            lo_slideshow_contr.send_slide_info()   # TODO check if this works
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
            lo_slideshow_contr.go_to_next_Slide()

        elif 'transition_previous' == action:
            lo_slideshow_contr.go_to_previous_Slide()

        elif 'goto_slide' == action:
            number = msg["number"]
            lo_slideshow_contr.goto_slide(number)

        elif 'presentation_start' == action:
            parent.start_presentation()

        elif 'presentation_stop' == action:
            parent.end_curent_presentation()

        # TODO add this function presentation_blank_screen
        elif 'presentation_blank_screen' == action:
            pass

        elif 'presentation_resume' == action:
            lo_slideshow_contr.resume_presentation()

    def on_close (self, reason):
        global clients
        clients.remove(self.ws)

        print("close", reason)

def run_irp_server(parent_, address = '0.0.0.0', port = 5100):
    addr = (address, port)
    global parent
    global lo_slideshow_contr
    parent = parent_
    lo_slideshow_contr = parent.lo_slideshow_contr
    WebSocketServer(addr, Resource(OrderedDict([('/', IRPApp)]))).serve_forever()

