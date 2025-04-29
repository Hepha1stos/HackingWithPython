from flask import render_template, request, Blueprint
from src.db import mysql

main_routes = Blueprint("main_routes",__name__)

@main_routes.route("/")
def homepage():
    cookie = request.cookies.get('name')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"SELECT username from users where username = '{cookie}'")
        name = cursor.fetchone()[0]
    except exec as e:
        name = ""
    print(name)
    
    return render_template('home.html', cookie=cookie, name=name)



