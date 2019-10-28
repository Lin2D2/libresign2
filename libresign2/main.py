
import time, logging, os, sys, multiprocessing, subprocess
import json
import libresign2.infoscreen.infoscreen as infoscreen

from libresign2.LibreOffice_Connection_Interface.LibreOffice_Setup_Connection import LibreOffice_Setup_Connection


class LibresignInstance():
    def __init__(self):
        self.settings_path = "settings.json"
        self.home_dir = self.read_settings("HomeDir")
        self.infoscreen_process = None
        self.network_addresse = None
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
                    if len(parameter) == len(value):
                        for p, v in parameter, value:
                            data[p] = v
                        json.dump(data, json_file)
                        logging.debug(["successful wrote", value, "to", parameter])
                elif type(parameter) == str:
                    data[parameter] = value
                    json.dump(data, json_file)
                    logging.debug(["successfully wrote", value, "to", parameter])
                else:
                    logging.warning(['write_settings didn\'t wrote', [parameter, type(parameter)], [value, type(value)]])
            except:
                logging.exception(["Unexpected error at writing settings:", sys.exc_info()[0], parameter, value])

    # TODO return True or False and logging.info()
    # TODO for now set to True
    def network_connection(self):
        return True

    def retry_network_connection(self):
        while not self.network_connection():
            logging.warning(["no network connection"])
            time.sleep(2)

    def run(self):
        if not self.network_connection():
            self.retry_network_connection()

        # TODO for now set to some url
        url = "http://google.com"
        self.infoscreen_process = multiprocessing.Process(target=infoscreen.start_info_screen, args=(url,))
        try:
            self.infoscreen_process.start()
            logging.info(["Infoscreen started"])
        except:
            logging.warning(["Infoscreen not started"])

        # TODO start Control sever

        cwd = os.getcwd()
        os.chdir(self.home_dir + '/web_control_panel')
        args = ['python3', '-m', 'http.server', self.read_settings("HTTP_PORT")]
        subprocess.Popen(args)

        os.chdir(cwd)

        # TODO start LibreOffice Instance

        self.lo_setup_conn.start_LibreOffice()
        self.lo_setup_conn.setup_LibreOffice_connection()

        self.lo_setup_conn.open_document_LibreOffice(
            '/home/linus/PycharmProjects/libresign2/libresign2/presentations/pre_file/Andras_Timar_LibOConf2011.odp')

        self.infoscreen_process.kill()
        self.lo_setup_conn.start_presentation()

        time.sleep(6)
        self.lo_setup_conn.lo_slideshow_contr.go_to_next_Slide()
        time.sleep(2)
        self.lo_setup_conn.end_curent_presentation()
        time.sleep(2)
        self.lo_setup_conn.close_document_LibreOffice()
        # TODO somehow kill the proc
        # LO_S_C.subprocess_libreoffice_pid.kill()

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
    # libresign_instance.write_settings(settings_to_write_parameter, settings_to_write_value)
    del settings_to_write_parameter, settings_to_write_value
    logging.info(["Setup completed", libresign_instance])
    libresign_instance.run()

setup()
