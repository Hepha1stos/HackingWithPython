from flask import render_template, request, Blueprint


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
    
    username = request.form.get("username")
    email = request.form.get("email")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    
    print(username,email,password1,password2)
    
    return render_template("register.html")
  return render_template("register.html")