from flask import Flask
from flask import render_template
from flask import request

from funcs.names import low

app = Flask(__name__)

@app.route("/main")
def main():
  vars= [low("Thorsten"),low("Johannah"),low("Fabian")]


  name = request.args.get("name","Test")
  return render_template("base.html", vars = vars, name=name)

@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/tickets")
def tickets_page():
    items= [{"id":1,"priority":2,"username":"Mark","title":"something broken"},
            {"id":2,"priority":4,"username":"Luke","title":"something working"},
            {"id":3,"priority":1,"username":"Thomas","title":"something waiting"}
            ]
    return render_template("tickets.html",items=items)

@app.route("/login",methods=["GET","POST"])
def user_login():
  if request.method == "POST":
    print("Post")
    
    username = request.form.get("username")
    password = request.form.get("password")
    print(username,password)
    return render_template("login.html")
  return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
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
if __name__ == "__main__":
  app.run(debug=True)