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

import os, time, sys, logging
import subprocess
import uno

from libresign2.web_control_panel.request import Request
from libresign2.LibreOffice_Connection_Interface.LibreOffice_SlideShow_Controlls import LibreOffice_SlideShow_Controlls
import irpjs.irp as irpjs


class LibreOffice_Setup_Connection():
    def __init__(self, parent=None):
        self.parent = parent
        self.p_cwd = self.parent.cwd
        self.subprocess_libreoffice_pid = None
        self.desktop = None
        self.docu = None
        self.current_filename = None
        self.setup_LibreOffice_connection_number_of_tries = 0
        self.lo_slideshow_contr = LibreOffice_SlideShow_Controlls(parent=self)

    def start_remote_sever(self):
        irpjs.run_irp_server(self)

    def start_LibreOffice(self):
        logging.info(['starting LibreOffice'])
        args = ["/usr/bin/soffice", '--nologo', '--norestore', '--nodefault', '--accept=pipe,name=libresign;urp']
        self.subprocess_libreoffice_pid = subprocess.Popen(args).pid
        # TODO somehow kill the proc after done
        logging.info(['subprocess for LibreOffice: ', self.subprocess_libreoffice_pid])
        # TODO sleep muss weg

    def setup_LibreOffice_connection(self):
        try:
            localContext = uno.getComponentContext()
            logging.debug(['setingup LibreOffice', localContext])
            resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext)
            logging.debug(['setingup LibreOffice', resolver])
            ctx = resolver.resolve('uno:pipe,name=libresign;urp;StarOffice.ComponentContext')
            logging.debug(['setingup LibreOffice', ctx])
            smgr = ctx.ServiceManager
            logging.debug(['setingup LibreOffice', smgr])
            self.desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
            logging.info(['setingup LibreOffice', self.desktop])
        except:
            self.setup_LibreOffice_connection_number_of_tries += 1
            time.sleep(1)
            logging.info("trying to connect to libreOffice")
            if self.setup_LibreOffice_connection_number_of_tries <= 20:
                self.setup_LibreOffice_connection()
            else:
                logging.warning("not able to connect to LibreOffice....... exiting..")
                sys.exit("quit because no connection to LibreOffice")

    def open_document_LibreOffice(self, file_path_url):
        self.docu = self.desktop.loadComponentFromURL("file://" + file_path_url, "MyFrame", 8, ())
        self.current_filename = file_path_url.split("/")[-1]

        # data = []
        # data.append(PropertyValue("OpenMode", 0, "open", DIRECT_VALUE))
        # data.append(PropertyValue("Hidden", 0, True, DIRECT_VALUE))
        # self.docu = self.desktop.loadComponentFromURL("file://" + file_path_url, "MyFrame", 8, data)

        # after the document is open this process will return True
        logging.debug(["self.docu", self.docu])
        return True

    def close_document_LibreOffice(self):
        self.docu.close(False)

    def start_presentation(self):
        logging.debug(['beginning to start presentation'])
        try:
            logging.debug(['beginning to start presentation', self.docu, self.docu.Presentation])
        except:
            logging.warning("failed logging self.docu and/or self.docu.Presentation")
        self.parent.infoscreen_process.kill()

        # self.docu.Presentation.IsAlwaysOnTop = True
        # self.docu.Presentation.IsEndless = False
        # self.docu.Presentation.IsFullScreen = True
        # self.docu.Presentation.IsMouseVisible = False
        # self.docu.Presentation.IsTransitionOnClick = False
        # self.docu.Presentation.Pause = 1
        self.docu.Presentation.start()
        logging.info('presentation started')

    def end_curent_presentation(self):
        model = self.desktop.getCurrentComponent()
        logging.debug(['get Current object, desktop, libreoffice', model])
        model.Presentation.end()

    def close_file (self):
        logging.debug(["funktion: close_file | in file: unoremote", self.docu])
        if self.docu:
            self.docu.dispose()
            self.docu = None

        logging.debug("close file")

    def playlist_changed (self):
        size = self.parent.playlist.get_playlist_size()

        newfile = self.parent.playlist.get_current()
        oldfile = self.current_filename

        if newfile != oldfile:
            self.close_file()
            self.parent.load_presentation(newfile)

        logging.debug("locontrol.py::playlist_changed()")

    def handle_web_request(self, msg):
        mtype = msg.get('type')
        logging.debug(["file type", mtype])

        if Request.QUEUE_FILE == mtype or Request.REMOVE_FILE == mtype:
            self.playlist_changed()

        if Request.PLAY_FILE == mtype:
            filename = msg.get('file')
            logging.debug(["before checking if file is not current file", "filename", filename])
            # TODO do you need this check
            # if filename != self.parent.playlist.get_current():
            #     logging.debug(["current file and filename", self.parent.playlist.get_current(), filename])
            #     self.parent.load_presentation(filename)
            self.parent.load_presentation(filename)

        if Request.PLAY == mtype:
            self.resume()

        if Request.PAUSE == mtype:
            self.pause()

