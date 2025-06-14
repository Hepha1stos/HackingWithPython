# src/auth_routes.py

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, send_file
from src.db import mysql
from src import limiter
import pyotp
import qrcode
import io

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per 1 minute", methods=["POST"])
def user_login():
    if request.method == "POST":
        conn = mysql.connect()
        cursor = conn.cursor()

        username = request.form.get("username")
        password = request.form.get("password")

        cursor.execute(
            "SELECT id, username, password, otp_secret FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user is None or user[2] != password:
            flash("Ungültige Zugangsdaten", "danger")
            return render_template("login.html"), 401

        # Zugangsdaten korrekt → Zwischenschritt: OTP prüfen
        session.clear()
        session["pre_2fa_user_id"] = user[0]
        session["pre_2fa_username"] = user[1]
        session["otp_secret"] = user[3]

        return redirect("/verify-otp")

    return render_template("login.html")


@auth_routes.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        otp = request.form.get("otp")
        otp_secret = session.get("otp_secret")

        if not otp_secret:
            flash("OTP nicht gefunden. Bitte erneut einloggen.", "danger")
            return redirect("/login")

        totp = pyotp.TOTP(otp_secret)
        if totp.verify(otp):
            # OTP korrekt → final einloggen
            session["user_id"] = session.pop("pre_2fa_user_id")
            session["username"] = session.pop("pre_2fa_username")
            session.pop("otp_secret", None)
            return redirect("/")
        else:
            flash("Ungültiger OTP-Code", "danger")
            return render_template("verify_otp.html"), 401

    return render_template("verify_otp.html")


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
            username  = request.form.get("username")
            email     = request.form.get("email")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            if password1 != password2:
                flash("Die Passwörter stimmen nicht überein", "danger")
                return render_template("register.html")

            # Neuen OTP-Secret generieren
            otp_secret = pyotp.random_base32()

            cursor.execute(
                "INSERT INTO users (username, email, password, otp_secret) VALUES (%s, %s, %s, %s)",
                (username, email, password1, otp_secret)
            )
            conn.commit()

            # NEU: Session direkt setzen, damit /setup-2fa funktioniert
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            session.clear()
            session["user_id"] = user[0]

            flash("Registrierung erfolgreich! Bitte richte deine 2FA ein.")
            return redirect("/setup-2fa")

        except Exception as e:
            conn.rollback()
            flash("Registrierung fehlgeschlagen: " + str(e), "danger")
            return render_template("register.html")
        finally:
            cursor.close()
            conn.close()

    return render_template("register.html")


@auth_routes.route("/setup-2fa")
def setup_2fa():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT username, otp_secret FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is None:
        flash("Benutzer nicht gefunden", "danger")
        return redirect("/login")

    username, otp_secret = result

    # OTP-Provisioning URI erstellen
    totp = pyotp.TOTP(otp_secret)
    uri = totp.provisioning_uri(name=username, issuer_name="MeineApp")

    # QR-Code generieren
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)

    return send_file(buf, mimetype='image/png')
