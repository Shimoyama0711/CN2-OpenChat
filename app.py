from io import BytesIO

from flask import Flask, render_template, request, session
import datetime
import mysql.connector as mydb
import hashlib
from PIL import Image
import base64


app = Flask(__name__)


# セッション機能を利用するために秘密鍵をセット
app.secret_key = "12345678901234567890123456789013"


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

        # SELECT
        cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
        user = cursor.fetchone()

        if user:
            msg = "このEメールアドレスは既に登録されています"
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
        avatar = "/static/img/anonymous.png"

        session["username"] = username

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

        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"UPDATE users SET username = '{username}', avatar = '{avatar}' WHERE email = '{email}'")
        conn.commit()

        cursor.close()
        conn.close()

        return render_template("settings.html", msg="設定の変更に成功しました", level="success")


# 部屋を新規作成するページ
@app.route("/create-new-room", methods=["GET", "POST"])
def create_new_room():
    method = request.method

    if method == "GET":
        return render_template("create-new-room.html")
    else:
        return "Coming soon..."



# 時間を取得するだけのテストAPI
@app.route("/time")
def time():
    now = datetime.datetime.now()
    return now.strftime("%Y/%m/%d %H:%M:%S"), 200


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

