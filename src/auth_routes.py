from flask import render_template, request, Blueprint,flash

from src.db import mysql


auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login",methods=["GET","POST"])
def user_login():
  if request.method == "POST":
    print("Post")

   
    username = request.form.get("username")
    password = request.form.get("password")
  

    print(username,password)
    return render_template("login.html")
  return render_template("login.html")


@auth_routes.route("/register",methods=["GET","POST"])
def user_register():
  if request.method == "POST":
    print("Post")
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
      username = request.form.get("username")
      email = request.form.get("email")
      password1 = request.form.get("password1")
      password2 = request.form.get("password2")
    except Exception as e:
      conn.rollback()
    finally:
      cursor.close()
      conn.close()
  
    print(username,email,password1,password2)
    
    cursor.execute(f"INSERT INTO users (username, email, password) VALUES ('{username}','{email}','{password2}')")
    conn.commit()


    return render_template("register.html")
  return render_template("register.html")