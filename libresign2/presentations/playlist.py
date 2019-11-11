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
        self.all_files  = []
        # files that are being played
        self.playlist   = []
        # current file index
        self.current    = 0

    # load previously-uploaded presentations
    def load_files (self):
        path = read_settings("SAVE_FOLDER")
        self.all_files = []
        logging.debug(["path to Save folder", cwd + path])
        for f in os.listdir(cwd + path):
            logging.debug(["path list dir", os.listdir(cwd + path)])
            if os.path.isfile(os.path.join(cwd + path, f)):
                item = {"file" : f}
                self.all_files.append(f)

        print("loaded presentation files", self.all_files)

    def load_playlist (self):
        path = read_settings("PLAYLIST")
        fd = open(cwd + path, "r")

        for line in fd:
            # TODO clean up !!!
            del self.playlist
            self.playlist = []
            self.playlist.append(line)

        fd.close()
        print("loaded playlist", self.playlist)
        return self.playlist

    # add file to playlist
    def queue_file(self, filename):
        logging.debug("queue_file run")
        for item in self.playlist:
            if item == filename:
                return
        path = read_settings("PLAYLIST")
        logging.debug(path)
        with open(cwd + path, "r") as file:
            logging.debug("queue_file check if alredy in playlist")
            for line in file:
                if line == filename:
                    return
        logging.debug("queue_file adding to playlist")
        self.playlist.append(filename)
        with open(cwd + path, "a") as file:
            file.write(filename)
            logging.debug("queue_file added to playlist")
            return

    # remove file from playlist
    def dequeue (self, filename):
        for item in self.playlist:
            if item == filename:
                del self.playlist[self.playlist.index(item)]
        path = read_settings("PLAYLIST")
        logging.debug(path)
        # TODO clean up !!!
        with open(cwd + path, "w") as file:
            logging.debug("queue_file check if alredy in playlist")
            if len(self.playlist) == 0:
                file.write("")
            for e in self.playlist:
                file.write(e + "\n")

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
