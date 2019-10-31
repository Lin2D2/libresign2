
from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True)
