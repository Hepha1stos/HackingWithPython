# src/auth_routes.py

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from src.db import mysql
from src import limiter  # ← wir holen genau die Instanz, die in src/__init__.py erzeugt wurde

auth_routes = Blueprint("auth_routes", __name__)

# Limit: Maximal 5 POST-Versuche pro 1 Minute pro IP
@auth_routes.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per 1 minute", methods=["POST"])
def user_login():
    if request.method == "POST":
        conn = mysql.connect()
        cursor = conn.cursor()

        username = request.form.get("username")
        password = request.form.get("password")

        # Plain-Text-Passwortabfrage wie vorher
        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user is None or user[2] != password:
            flash("Ungültige Zugangsdaten", "danger")
            return render_template("login.html"), 401

        # Login erfolgreich
        session.clear()
        session["user_id"] = user[0]
        session["username"] = user[1]
        return redirect("/")

    return render_template("login.html")


@auth_routes.route("/logout")
def user_logout():
    session.clear()
    return redirect("/login")


@auth_routes.route("/register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            username = request.form.get("username")
            email    = request.form.get("email")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            if password1 != password2:
                flash("Die Passwörter stimmen nicht überein")
                return render_template("register.html")

            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password1)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            flash("Registrierung fehlgeschlagen: " + str(e))
            return render_template("register.html")
        finally:
            cursor.close()
            conn.close()

        return redirect("/login")

    return render_template("register.html")
