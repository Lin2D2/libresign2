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
        self.all_files  = []
        # files that are being played
        self.playlist   = []
        # current file index
        self.current    = 0

    @staticmethod
    def allowed_format(file):
        allowed_formats = ["odp", "pptx", "ppt"]
        if re.split("\.", file)[-1] in allowed_formats:
            return True
        else:
            return False

    # load previously-uploaded presentations
    def load_files (self):
        path = read_settings("SAVE_FOLDER")
        self.all_files = []
        logging.debug(["path to Save folder", cwd + path])
        for pre_file in os.listdir(cwd + path):
            logging.debug(["path list dir", os.listdir(cwd + path)])
            if os.path.isfile(os.path.join(cwd + path, pre_file)):
                if self.allowed_format(pre_file):
                    self.all_files.append(pre_file)
                else:
                    logging.warning([pre_file, "is not an allowed format"])

        print("loaded presentation files", self.all_files)
        return self.all_files

    def load_playlist (self):
        path = read_settings("PLAYLIST")
        with open(cwd + path, "r") as playlist_file:
            del self.playlist
            self.playlist = []

            for line in playlist_file:
                if self.allowed_format(line):
                    self.playlist.append(line)
                else:
                    # TODO warn the user if an file type is not supported
                    pass

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
