
import os, time, sys, logging
import subprocess, base64
import uno
import unohelper


class LibreOffice_SlideShow_Controlls():
    def __init__(self, parent=None):
        self.parent = parent

    def go_to_next_Slide(self):
        self.parent.docu.Presentation.Controller.gotoNextSlide()

    def go_to_previous_Slide(self):
        self.parent.docu.Presentation.Controller.gotoPreviousSlide()