from flask import Flask, render_template
import datetime


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html"), 200


@app.route("/login")
def login():
    return render_template("login.html"), 200


@app.route("/time")
def time():
    now = datetime.datetime.now()
    return now.strftime("%Y/%m/%d %H:%M:%S"), 200


@app.route("/navbar")
def navbar():
    return render_template("navbar.html"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

