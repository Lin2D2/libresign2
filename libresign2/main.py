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

import time, logging, os, sys, multiprocessing, subprocess , threading
import json, queue, signal
import ifcfg   # TODO pip3 install ifcfg

from flask import Flask

from libresign2.presentations.playlist import Playlist
from libresign2.LibreOffice_Connection_Interface.LibreOffice_Setup_Connection import LibreOffice_Setup_Connection
import libresign2.infoscreen.infoscreen as infoscreen


class LibresignInstance():
    def __init__(self):
        self.cwd = os.getcwd()
        self.settings_path = self.cwd + "/libresign2/settings.json"
        self.write_settings("HomeDir", self.cwd)
        self.home_dir = self.cwd
        self.infoscreen_process = None
        self.remote_sever_proc = None
        self.messages = queue.Queue()
        self.playlist = Playlist()
        self.ip_addr = self.get_ip_addr()
        self.lo_setup_conn = LibreOffice_Setup_Connection(parent=self)

    def read_settings(self, parameter):
        with open(self.settings_path, "r") as json_file:
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

    def write_settings(self, parameter, value):
        with open(self.settings_path, "r") as json_file:
            data = json.load(json_file)
        with open(self.settings_path, "w") as json_file:
            try:
                # add that you can do more then just write more than one parameter
                if type(parameter) == list and type(value) == list:
                    if len(parameter) >= 1 and len(value) >= 1:
                        if len(parameter) == len(value):
                            i = 0
                            while i < len(parameter):
                                data[parameter[i]] = value[i]
                                i += 1
                            json.dump(data, json_file)
                            logging.debug(["successful wrote", value, "to", parameter])
                            return
                    else:
                        if len(parameter) != 0 and len(value) != 0:
                            parameter = parameter[0]
                            value = value[0]
                        else:
                            logging.warning(['write_settings didn\'t wrote', [parameter, type(parameter)], [value, type(value)]])
                            json.dump(data, json_file)
                            return
                if type(parameter) == str:
                    data[parameter] = value
                    json.dump(data, json_file)
                    logging.debug(["successfully wrote", value, "to", parameter])
                else:
                    logging.warning(['write_settings didn\'t wrote', [parameter, type(parameter)], [value, type(value)]])
                    json.dump(data, json_file)
                    return
            except:
                logging.exception(["Unexpected error at writing settings:", sys.exc_info()[0], parameter, value])

    def get_ip_addr(self):
        return ifcfg.default_interface()["inet"]

    # TODO return True or False and logging.info()
    # TODO for now set to True
    def network_connection(self):
        return True

    def retry_network_connection(self):
        while not self.network_connection():
            logging.warning(["no network connection"])
            time.sleep(2)

    def get_playlist (self):
        return self.playlist

    def load_presentation(self, file):
        try:
            self.lo_setup_conn.open_document_LibreOffice(
                self.cwd + self.read_settings("SAVE_FOLDER") + "/" + file)
            return True
        except:
            logging.warning("failed to load presentation")
            return False

    def run(self):
        try:
            os.mkdir(self.cwd + "/libresign2/presentations/pre_file")
        except FileExistsError:
            pass
        with open(self.cwd + "/libresign2/presentations/playlist", "w+"):
            pass

        if not self.network_connection():
            self.retry_network_connection()

        logging.info(['ip addresse:', self.ip_addr])

        # start info screen
        url = "http://" + self.ip_addr + ":5000"
        self.infoscreen_process = multiprocessing.Process(
            target=infoscreen.start_info_screen,
            args=(url,))
        try:
            self.infoscreen_process.start()
            logging.info(["Infoscreen started"])
        except:
            logging.warning(["Infoscreen not started"])

        # start LibreOffice Instance
        self.lo_setup_conn.start_LibreOffice()
        self.lo_setup_conn.setup_LibreOffice_connection()

        # start remote sever
        app = Flask("libresign")
        self.remote_sever_proc = multiprocessing.Process(
            target=self.lo_setup_conn.start_remote_sever,
            args=(app, self.ip_addr, "5000"))
        try:
            self.remote_sever_proc.start()
            logging.info(["remote_sever started"])
        except:
            logging.warning(["remote_sever not started"])

        # load presentations

        self.playlist.load_files()
        self.playlist.load_playlist()

        # TODO add an option to quit to Program


def setup():
    args = sys.argv
    settings_to_write_parameter = []
    settings_to_write_value = []
    for i in range(len(args)):
        arg = args[i]

        # don't show the fullscreen info screen
        if arg == '--noinfo':
            settings_to_write_parameter.append("SHOW_INFO_SCREEN")
            settings_to_write_value.append(False)

        # default anyway
        if arg == '--conference':
            settings_to_write_parameter.append("CONFERENCE")
            settings_to_write_value.append(True)

        # change home dir
        if arg == '--libresign-home':
            if os.path.isdir(args[i + 1]):
                settings_to_write_parameter.append("HomeDir")
                settings_to_write_value.append(args[i + 1])
                i += 1
                logging.info('libresign home', settings_to_write_value[-1])
            else:
                logging.warning('libresign home', settings_to_write_value[-1])

    libresign_instance = LibresignInstance()
    logging_level = libresign_instance.read_settings('LOGGING_LEVEL')
    logging.root.setLevel(logging_level)
    logging.info(['Libresign Instance created', 'sys.args=', args[1:]])
    libresign_instance.write_settings("HomeDir", os.path.dirname(os.path.realpath(__file__)))
    # TODO write settings from above to settings.json
    libresign_instance.write_settings(settings_to_write_parameter, settings_to_write_value)
    del settings_to_write_parameter, settings_to_write_value
    logging.info(["Setup completed", libresign_instance])
    libresign_instance.run()
