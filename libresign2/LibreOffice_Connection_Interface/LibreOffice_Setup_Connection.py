
import os, time, sys, logging
import subprocess, base64
import uno
import unohelper

from com.sun.star.beans import PropertyValue
from com.sun.star.beans.PropertyState import DIRECT_VALUE

from libresign2.LibreOffice_Connection_Interface.LibreOffice_SlideShow_Controlls import LibreOffice_SlideShow_Controlls


class LibreOffice_Setup_Connection():
    def __init__(self, parent=None):
        self.parent = parent
        self.p_cwd = self.parent.cwd
        self.subprocess_libreoffice_pid = None
        self.desktop = None
        self.docu = None
        self.lo_slideshow_contr = LibreOffice_SlideShow_Controlls(parent=self)

    def start_LibreOffice(self):
        logging.info(['starting LibreOffice'])
        args = ["/usr/bin/soffice", '--nologo', '--norestore', '--nodefault', '--accept=pipe,name=libresign;urp']
        self.subprocess_libreoffice_pid = subprocess.Popen(args).pid
        # TODO somehow kill the proc after done
        logging.info(['subprocess for LibreOffice: ', self.subprocess_libreoffice_pid])
        logging.info(['sleeping', 1])
        time.sleep(1)
        # TODO sleep muss weg

    def setup_LibreOffice_connection(self):
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

    def open_document_LibreOffice(self, file_path_url):
        self.docu = self.desktop.loadComponentFromURL("file://" + file_path_url, "MyFrame", 8, ())

        # data = []
        # data.append(PropertyValue("OpenMode", 0, "open", DIRECT_VALUE))
        # data.append(PropertyValue("Hidden", 0, True, DIRECT_VALUE))
        # self.docu = self.desktop.loadComponentFromURL("file://" + file_path_url, "MyFrame", 8, data)

        # after the document is open this process will return True
        return True

    def close_document_LibreOffice(self):
        self.docu.close(False)

    def start_presentation(self):
        self.docu.Presentation.IsAlwaysOnTop = True
        self.docu.Presentation.IsEndless = False
        self.docu.Presentation.IsFullScreen = True
        self.docu.Presentation.IsMouseVisible = False
        self.docu.Presentation.IsTransitionOnClick = False
        self.docu.Presentation.Pause = 1
        self.docu.Presentation.start()
        logging.info('presentation started')

    def end_curent_presentation(self):
        model = self.desktop.getCurrentComponent()
        logging.debug(['get Current object, desktop, libreoffice', model])
        model.Presentation.end()


# logging.root.setLevel(10)

# lo_setup_conn = LibreOffice_Setup_Connection()
# lo_setup_conn.start_LibreOffice()
# lo_setup_conn.setup_LibreOffice_connection()
#
# lo_setup_conn.open_document_LibreOffice('/home/linus/PycharmProjects/libresign2/libresign2/presentations/pre_file/Andras_Timar_LibOConf2011.odp')
#
# lo_setup_conn.start_presentation()
#
# time.sleep(6)
# lo_setup_conn.lo_slideshow_contr.go_to_next_Slide()
# time.sleep(2)
# lo_setup_conn.end_curent_presentation()
# time.sleep(2)
# lo_setup_conn.close_document_LibreOffice()
# # TODO somehow kill the proc
# # LO_S_C.subprocess_libreoffice_pid.kill()
