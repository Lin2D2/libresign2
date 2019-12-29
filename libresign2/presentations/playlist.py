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
import json
import logging
import os
import sys
import re
import datetime
import threading

#TODO full rewrite of this file... just for better implementing of settings and new playlist functions.

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


class Playlist():
    def __init__ (self):
        # all files that have been uploaded
        self.uploaded_presentations  = []
        # files that are being played
        self.playlist   = []
        # current file index
        self.current    = 0

    @staticmethod
    def allowed_format(file):
        allowed_formats = ["odp", "pptx", "ppt"]
        file = re.split("\n", file)[0]
        if re.split("\.", file)[-1] in allowed_formats:
            return True
        else:
            return False

    # load previously-uploaded presentations
    def load_files (self):
        path = read_settings("SAVE_FOLDER")
        self.uploaded_presentations = []
        logging.debug(["path to Save folder", cwd + path])
        for pre_file in os.listdir(cwd + path):
            logging.debug(["path list dir", os.listdir(cwd + path)])
            if os.path.isfile(os.path.join(cwd + path, pre_file)):
                if self.allowed_format(pre_file):
                    self.uploaded_presentations.append(pre_file)
                else:
                    logging.warning([pre_file, "is not an allowed format"])

        print("loaded presentation files", self.uploaded_presentations)
        return self.uploaded_presentations

    def load_playlist (self):
        path = read_settings("PLAYLIST")
        with open(cwd + path, "r") as playlist_file:
            del self.playlist
            self.playlist = []
            lines = playlist_file.readlines()
            logging.warning(lines)
            for line in lines:
                if self.allowed_format(line):
                    self.playlist.append(line)
                else:
                    # TODO warn the user if an file type is not supported
                    pass

        print("loaded playlist", self.playlist)
        return self.playlist

    def queue_file(self, filename):
        path = read_settings("PLAYLIST")
        if filename not in self.playlist:
            self.playlist.append(filename)

        def queue_file_write():
            with open(cwd + path , "r") as file:
                r_file = file.readlines()
            if filename not in r_file:
                with open(cwd + path, "w") as file:
                    file_content = []
                    file_content.append(str(datetime.datetime.now()))
                    file_content.append("\n")
                    for e in self.playlist:
                        file_content.append("\n" + e)
                    file.writelines(file_content)
        threading.Thread(target=queue_file_write).start()
        return self.playlist

    # remove file from playlist
    def dequeue(self, filename):
        path = read_settings("PLAYLIST")
        if filename in self.playlist:
            del self.playlist[self.playlist.index(filename)]

        def dequeue_write():
            with open(cwd + path, "r") as file:
                r_file = file.readlines()
                _file = []
                for e in r_file:
                    _file.append(re.split("\n", e)[0])
            if filename in _file:
                del r_file[_file.index(filename)]
                with open(cwd + path, "w") as file:
                    file.writelines(r_file)
        threading.Thread(target=dequeue_write).start()
        return self.playlist

    # select file to be played right now
    def select_file (self, filename):
        c = 0

        for item in self.playlist:
            if item.get("file") == filename:
                self.current = c
                break

            c += 1

        print("play", self.current, filename)

    # return filename of current presentation to be played
    def get_current (self):
        if len(self.playlist) > self.current:
            return self.playlist[self.current]['file']
        else:
            return None
