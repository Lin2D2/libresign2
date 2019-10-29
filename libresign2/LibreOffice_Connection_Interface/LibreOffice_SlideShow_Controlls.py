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
import subprocess, base64
import uno
import unohelper


class LibreOffice_SlideShow_Controlls():
    def __init__(self, parent=None):
        self.parent = parent

    def send_slide_info (self):
        pass

    def go_to_next_Slide(self):
        self.parent.docu.Presentation.Controller.gotoNextSlide()

    def go_to_previous_Slide(self):
        self.parent.docu.Presentation.Controller.gotoPreviousSlide()

    # TODO add this function goto_slide(number)
    def goto_slide(self, number):
        pass

    # TODO add this function presentation_resume
    def resume_presentation(self):
        pass
