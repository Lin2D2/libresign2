
from flask import Flask, render_template
import logging

# TODO look here for how to create the app https://github.com/flaskbb/flaskbb/blob/master/flaskbb/app.py

def routes(app, parent):
    @app.route("/")
    def home():
        return render_template("control_panel.html")

    @app.route("/impress_remote")
    def impress_remote():
        return render_template("impress_remote.html",
                                presentation="stuff.odp",
                                presentation_status="playing",
                                connection_status="connected"
                                )

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/impress_remote/close")
    def close():
        global parent
        parent.close_file()

    @app.route("/impress_remote/preview")
    def preview():
        pass

    @app.route("/impress_remote/play")
    def play():
        pass

    @app.route("/impress_remote/reverse_reverse")
    def reverse_reverse():
        parent.lo_slideshow_contr.go_to_previous_Slide()

    @app.route("/impress_remote/reverse")
    def reverse():
        pass

    @app.route("/impress_remote/forward")
    def forward():
        pass

    @app.route("/impress_remote/forward_forward")
    def forward_forward():
        parent.lo_slideshow_contr.go_to_next_Slide()

    @app.route("/impress_remote/refresh")
    def refresh():
        pass


def run(parent, app, url, port):
    routes(app, parent)
    app.run(debug=True, host=url, port=port, threaded=True)
    # TODO the problem is the restart of the application "INFO:werkzeug: * Restarting with stat"
    # TODO some how fix the restart ! it should not restart !!!

#
# run(None, "192.168.110.141", "5000")
