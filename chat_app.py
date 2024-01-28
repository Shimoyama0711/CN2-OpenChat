from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)

# セッション機能を利用するために秘密鍵をセット
app.secret_key = "1234567890abcdef1234567890abcdef"

# リアルタイム更新のためにSocketIOを使う
socketio = SocketIO(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("chat-test.html")


@socketio.on("send_message")
def handle_message(data):
    print("TRIGGERED!! :)")
    message = data["message"]
    socketio.emit("receive_message", {'message': message})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, log_output=True, use_reloader=True)
