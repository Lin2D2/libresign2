
from flask import Flask, render_template

app = Flask(__name__)


class FlaskApp():
    def __init__(self):
        pass

    @app.route("/")
    def home(self):
        return render_template("control_panel.html")

    @app.route("/impress_remote")
    def impress_remote(self):
        return render_template("impress_remote.html",
                               presentation="stuff.odp",
                               presentation_status="playing",
                               connection_status="connected"
                               )

    @app.route("/about")
    def about(self):
        return render_template("about.html")

    @app.route("/impress_remote/close")
    def close(self):
        pass

    @app.route("/impress_remote/preview")
    def preview(self):
        pass

    @app.route("/impress_remote/play")
    def play(self):
        pass

    @app.route("/impress_remote/reverse_reverse")
    def reverse_reverse(self):
        pass

    @app.route("/impress_remote/reverse")
    def reverse(self):
        pass

    @app.route("/impress_remote/forward")
    def forward(self):
        pass

    @app.route("/impress_remote/forward_forward")
    def forward_forward(self):
        pass

    @app.route("/impress_remote/refresh")
    def refresh(self):
        pass


if __name__ == "__main__":
    app.run(debug=True)
