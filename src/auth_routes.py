from flask import render_template, request, Blueprint,flash, redirect

from src.db import mysql


auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login",methods=["GET","POST"])
def user_login():
  if request.method == "POST":
    print("Post")

    conn = mysql.connect()
    cursor = conn.cursor()
   
    username = request.form.get("username")
    password = request.form.get("password")
  
    query = f"SELECT username from users WHERE username = '{username}' AND password = '{password}'"
    print(query)
    cursor.execute(query)

    result = cursor.fetchone()[0]
    if not result:
      return render_template("login.html", cookie=None)

    resp = redirect("/")
    resp.set_cookie("name",username)
    return resp
  return render_template("login.html")

@auth_routes.route("/logout")
def user_logout():
  resp = redirect("/login")
  resp.set_cookie("name",'',expires=0)
  return resp

@auth_routes.route("/register",methods=["GET","POST"])
def user_register():
  if request.method == "POST":
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
      username = request.form.get("username")
      email = request.form.get("email")
      password1 = request.form.get("password1")
      password2 = request.form.get("password2")

      cursor.execute(f"INSERT INTO users (username, email, password) VALUES ('{username}','{email}','{password2}')")
      conn.commit()

    except Exception as e:
      conn.rollback()
    finally:
      cursor.close()
      conn.close()
    
    return render_template("login.html", cookie=None)
  return render_template("register.html", cookie=None)