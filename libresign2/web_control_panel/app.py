
from flask import Flask, render_template

parent = None
app = Flask(__name__)


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


def run(parent_, url, port):
    global parent
    parent = parent_
    app.run(debug=True, host=url, port=port)

#
# run(None, "192.168.110.141", "5000")
