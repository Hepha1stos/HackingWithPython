from flask import render_template, request, Blueprint,flash,redirect

from src.db import mysql


auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login",methods=["GET","POST"])
def user_login():
  if request.method == "POST":
    print("Post")

   
    username = request.form.get("username")
    password = request.form.get("password")
  
    query = f"SELECT username FROM users where username='{username}' AND password ='{password}'"

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(query)

    user = cursor.fetchone()
    

    if user:
      print("Erfolg")
      resp = redirect("/overview")
      resp.set_cookie(key="name",value=user[0])
      return resp
    else:
        return redirect("/")
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