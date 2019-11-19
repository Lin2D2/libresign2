
import logging
import os

from flask import Flask, render_template, redirect, request


# Note for dev:look here for how to create the app https://github.com/flaskbb/flaskbb/blob/master/flaskbb/app.py


def routes(app, parent):
    @app.route("/")
    def home():
        return render_template("control_panel.html",
                               files=os.listdir(parent.pre_file_dir),
                               playlist_items=parent.parent.playlist.load_playlist()
                               )

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

    @app.route("/upload", methods=['POST'])
    def handleFileUpload():
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file.save(os.path.join(parent.pre_file_dir, file.filename))
        return redirect("/")

    # @app.route('/get_uploads/<uploads>', methods=['GET'])
    # def get_file():
    #     uploads = os.listdir('/home/space/Documents/libresign/development/libresign2/presentations/pre_file')
    #     return 'User %s' % escape("uploads")

    @app.route("/request/<action>/<data>")
    def request_(action, data):
        logging.debug(action)
        logging.debug(data)
        if action == "add":
            playlist_add(data)
        if action == "Download":
            logging.debug("download")
        if action == "play":
            parent.open_document_LibreOffice(data)
        if action == "remove":
            playlist_remove(data)
        return redirect("/")

    @app.route("/impress_remote/close")
    def close():
        global parent
        parent.close_file()

    @app.route("/impress_remote/preview")
    def preview():
        pass

    @app.route("/impress_remote/play")
    def play():
        parent.start_presentation()
        return redirect("/impress_remote")

    @app.route("/impress_remote/reverse_reverse")
    def reverse_reverse():
        parent.lo_slideshow_contr.go_to_previous_Slide()
        return redirect("/impress_remote")

    @app.route("/impress_remote/reverse")
    def reverse():
        pass

    @app.route("/impress_remote/forward")
    def forward():
        pass

    @app.route("/impress_remote/forward_forward")
    def forward_forward():
        parent.lo_slideshow_contr.go_to_next_Slide()
        return redirect("/impress_remote")

    @app.route("/impress_remote/refresh")
    def refresh():
        pass

    def playlist_add(data):
        parent.parent.playlist.queue_file(data)

    def playlist_remove(data):
        parent.parent.playlist.dequeue(data)


def run(parent, url, port):
    app = Flask(__name__)
    routes(app, parent)
    debug = parent.parent.settings_dict["DEBUG"]
    app.run(debug=debug, host=url, port=port, threaded=True, use_reloader=False)
#     app.run(debug=True, host=url, port=port, threaded=True, use_reloader=True)
#
#
# run(None, "192.168.178.73", "5000")
