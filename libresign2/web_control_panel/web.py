# Version: MPL 1.1
#
# This file is part of the LibreOffice project.
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# Contributor(s):
# Rasmus P J <wasmus@zom.bi>
#
# This is the control panel backend.
# Using the development web server now but Flask is 
# apparently compatible with most/all web servers
#

import threading, logging, subprocess, os, json, sys

import libresign2.web_control_panel.request as request
import libresign2.web_control_panel.flaskapp as flaskapp


cwd = os.getcwd()
settings_path = cwd + "/libresign2/settings.json"

def read_settings(parameter):
    with open(settings_path, "r") as json_file:
        data = json.load(json_file)
        try:
            # add that you can do more then just reading one parameter at a time
            if type(parameter) == list:
                result = []
                for p in parameter:
                    result.append(data[p])
                return result
            elif type(parameter) == str:
                return data[parameter]
            else:
                logging.warning(['read_settings, return None', [parameter, type(parameter)]])
                return None
        except:
            logging.exception(["Unexpected error at reading settings:", sys.exc_info()[0], parameter])

# TODO wrap this up into a class

msg_queue = None
running = None
thread = None
files = []
signd = None


def start(signd_, msgs):
    global msg_queue, running, thread, signd

    signd = signd_

    if not running:
        msg_queue = msgs
        running = True
        thread = threading.Thread(target=web_thread, args=())
        thread.setDaemon(True)
        thread.start()


def stop():
    # TODO use other server than werkzeug and deal with shutdown at that point
    pass


class WebPusher():
    def push_request (self, request):
        global msg_queue

        if msg_queue:
            msg_queue.put(request)

    def get_playlist (self):
        playlist = signd.get_playlist()
        return playlist.playlist

    def get_all_files (self):
        playlist = signd.get_playlist()
        return playlist.all_files

    def get_current_playlist_item (self):
        playlist = signd.get_playlist()
        return playlist.get_current()

    def get_address(self):
        return get_address()


def web_thread():
    web = WebPusher()
    logging.info("starting web server")
    flaskapp.run(web)
    logging.info("stopping web server")


def get_addr_1():
    # NOTE linux only -- best i could do
    p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    # TODO might be errors?
    addr, err = p.communicate()
    p.wait()

    logging.debug("web.py::get_addr_1(): hostname -I output: " + str(addr))

    # output of hostname something like "b'123.0.0.123 x.x.x.x y.y.y.y\n"
    addr = str(addr).split(' ')[0]
    addr = ''.join([c for c in addr if c.isdigit() or c == '.'])

    logging.debug("web::get_addr_1(): got addr " + addr)

    return addr


def get_address():
    port = read_settings("HTTP_PORT")
    addr = get_addr_1()

    return addr
