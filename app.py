import json
from io import BytesIO
import datetime
import hashlib
import base64
import random

from flask import Flask, render_template, request, session, redirect, jsonify
from flask_socketio import SocketIO, join_room
import mysql.connector as mydb
from PIL import Image

from room import Room
from player import Player


app = Flask(__name__)


# セッション機能を利用するために秘密鍵をセット
app.secret_key = "1234567890abcdef1234567890abcdef"

# リアルタイム更新のためにSocketIOを使う
socketio = SocketIO(app)

# 部屋の一覧
# ここには room を入れます
# {
#     room_number: <room object>
# }
rooms = {}


# SHA-256に変換
def to_sha256(input_string):
    # 文字列をUTF-8でエンコード
    encoded_string = input_string.encode('utf-8')

    # SHA-256ハッシュオブジェクトを作成
    sha256_hash = hashlib.sha256()

    # ハッシュオブジェクトに文字列を渡して更新
    sha256_hash.update(encoded_string)

    # ハッシュ値を16進数文字列で取得
    hashed_string = sha256_hash.hexdigest()

    return hashed_string


# ユーザー名からアバターを取得
def get_avatar_from_username(username):
    conn = mydb.connect(
        host='localhost',
        port='3306',
        user='root',
        password='BTcfrLkK1FFU',
        database='werewolf'
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return user["avatar"]
    else:
        return "/static/img/anonymous.png"


# /index
# index.html を表示します
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html"), 200


# サインアップ機能です
@app.route("/signup", methods=["GET", "POST"])
def signup():
    method = request.method

    if method == "GET":
        return render_template("signup.html"), 200
    else:
        form = request.form
        msg = "サインアップに成功しました"

        conn = mydb.connect(
            host='localhost',
            port='3306',
            user='root',
            password='BTcfrLkK1FFU',
            database='werewolf'
        )

        email = form.get("email")
        username = form.get("username")
        password = to_sha256(form.get("password"))

        cursor = conn.cursor(dictionary=True)

        # Eメールアドレスが既に登録されているかチェック
        cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
        email_check = cursor.fetchone()

        # ユーザー名が既に登録されているかチェック
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
        username_check = cursor.fetchone()

        if email_check:
            msg = "そのEメールアドレスは既に登録されています"
            return render_template("signup.html", msg=msg, level="danger"), 400
        elif username_check:
            msg = "そのユーザー名は既に登録されています"
            return render_template("signup.html", msg=msg, level="danger"), 400
        else:
            cursor.execute(f"INSERT IGNORE INTO users VALUES ('{email}', '{username}', '{password}', '0', '0', '/static/img/anonymous.png')")
            conn.commit()
            cursor.close()

            session["loggedin"] = True
            session["email"] = email
            session["username"] = username

            return render_template("index.html", msg=msg, level="success")


# ログイン機能です
@app.route("/login", methods=["GET", "POST"])
def login():
    method = request.method

    if method == "GET":
        return render_template("login.html"), 200
    else:
        form = request.form

        conn = mydb.connect(
            host='localhost',
            port='3306',
            user='root',
            password='BTcfrLkK1FFU',
            database='werewolf'
        )

        email = form.get("email")
        password = to_sha256(form.get("password"))

        cursor = conn.cursor(dictionary=True)

        # SELECT
        cursor.execute(f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'")
        user = cursor.fetchone()
        conn.commit()
        cursor.close()

        if user:
            msg = "ログインに成功しました"

            session["loggedin"] = True
            session["email"] = user["email"]
            session["username"] = user["username"]

            return render_template("index.html", msg=msg, level="success"), 200
        else:
            msg = "Eメールアドレス または パスワード が違います"
            return render_template("login.html", msg=msg, level="danger"), 400


# ログアウトしてセッションを削除します
@app.route("/logout", methods=["GET", "POST"])
def logout():
    msg = "ログアウトしました"

    session["loggedin"] = False
    session["email"] = ""
    session["username"] = ""

    return render_template("index.html", msg=msg, level="success"), 200


# 設定画面
@app.route("/settings", methods=["GET", "POST"])
def settings():
    conn = mydb.connect(
        host="localhost",
        port=3306,
        user="root",
        password="BTcfrLkK1FFU",
        database="werewolf"
    )

    method = request.method

    if method == "GET":
        return render_template("settings.html", msg="", level="success")
    elif method == "POST":
        form = request.form

        email = session["email"]
        username = form.get("username")

        cursor = conn.cursor(dictionary=True)

        if len(username) > 0:
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
            user = cursor.fetchone()

            if user:
                return render_template("settings.html", msg="そのユーザー名は既に登録されています")
            else:
                session["username"] = username
                cursor.execute(f"UPDATE users SET username = '{username}' WHERE email = '{email}'")

        avatar = "/static/img/anonymous.png"

        if 'avatar' in request.files:
            image_file = request.files['avatar']

            if image_file.filename != '':
                img = Image.open(image_file)
                img_resized = img.resize((48, 48))

                buffered = BytesIO()
                img_resized.save(buffered, format="PNG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

                avatar = f"data:image/png;base64,{base64_image}"

                # ここでbase64形式のデータを使って何かしらの処理を行うことができます
                # print(avatar)

                cursor.execute(f"UPDATE users SET avatar = '{avatar}' WHERE email = '{email}'")

        conn.commit()

        cursor.close()
        conn.close()

        return render_template("settings.html", msg="設定の変更に成功しました", level="success")


# 部屋を新規作成するページ
@app.route("/create-new-room")
def create_new_room():
    method = request.method

    # 部屋番号抽選
    # 既に作成済みの部屋番号でなければループを抜ける
    while True:
        room_number = random.randint(0, 9999)
        formatted_number = "{:04d}".format(room_number)

        if formatted_number not in rooms:
            room_object = Room(formatted_number, 3, 60, 2, 1, 0)
            rooms[formatted_number] = room_object

            username = session["username"]
            avatar = get_avatar_from_username(username)

            # プレイヤーの定義
            player = Player(username, avatar, "unknown")

            # 部屋作成者はオーナーとなる
            player.is_owner = True

            # プレイヤーを部屋に追加
            rooms[formatted_number].add_player(player)

            break

    return redirect(f"/game/{formatted_number}")


# ゲーム部屋
@app.route("/game/<string:room_number>")
def game(room_number):
    if room_number not in rooms:
        return render_template("error.html", title="Bad Room Number", code=400, msg="この部屋番号は存在しません")
    else:
        username = session["username"]
        avatar = get_avatar_from_username(username)

        # プレイヤーの定義
        player = Player(username, avatar, "unknown")

        # プレイヤーを追加
        rooms[room_number].add_player(player)

        return render_template("lobby.html", room_number=room_number, room=rooms[room_number])


# 時間を取得するだけのテストAPI
@app.route("/time")
def time():
    now = datetime.datetime.now()
    return now.strftime("%Y/%m/%d %H:%M:%S"), 200


# 部屋の状態確認（デバッグ）
@app.route("/get-rooms")
def get_rooms():
    return str(rooms), {
        "Content-Type": "text/plain"
    }


@app.route("/debug-lobby")
def debug_lobby():
    return render_template("lobby.html")


# navbar です
@app.route("/navbar")
def navbar():
    try:
        email = session["email"]

        if email is None:
            return render_template("navbar.html"), 200
        else:
            conn = mydb.connect(
                host='localhost',
                port='3306',
                user='root',
                password='BTcfrLkK1FFU',
                database='werewolf'
            )

            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                avatar = user["avatar"]
                return render_template("navbar.html", avatar=avatar), 200
            else:
                return render_template("navbar.html"), 200
    except KeyError:
        return render_template("navbar.html"), 200


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", title="Not Found", code=404, msg="あなたが探しているページは見つかりませんでした。"), 404


@socketio.on('join')
def on_join(data):
    print("ON JOIN! :)")

    room_number = data["room_number"]
    players = rooms[room_number].players

    # Playerオブジェクトを辞書型に変換
    players_data = [player.to_dict() for player in players]

    # 辞書型に変換されたプレイヤーデータをクライアントに送信
    socketio.emit("update_room", {"room_number": room_number, "players": players_data})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, log_output=True, use_reloader=True)
