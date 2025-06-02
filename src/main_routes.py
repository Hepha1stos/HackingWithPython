from flask import render_template, session, redirect, url_for, Blueprint
from src.db import mysql

main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/")
def homepage():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth_routes.user_login"))

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()  # liefert z. B. ("admin",)
    cursor.close()
    conn.close()

    if not user:
        session.clear()
        return redirect(url_for("auth_routes.user_login"))

    name = user[0]
    return render_template("home.html", username=name)
