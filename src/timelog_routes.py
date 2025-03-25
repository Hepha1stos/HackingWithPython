from flask import render_template, request, Blueprint

from src.db import mysql

timelog_routes = Blueprint("timelog_routes", __name__)


@timelog_routes.route("/overview")
def show():
    conn = mysql.connect()
    cursor = conn.cursor()  
    cursor.execute("SELECT t.*, c.name,u.username  FROM timelog as t JOIN category c ON t.category_id = c.id JOIN users u ON t.user_id = u.id ORDER BY t.date;")
    logs = cursor.fetchall()
    print(logs)
    parsedLogs = [
        {
            "id": row[0],
            "time": str(row[1]),
            "date": row[2].strftime("%d.%m.%Y"),
            "category": row[5],
            "user": row[6]
        }
        for row in logs
    ]

    
    return render_template("overview.html",logs=parsedLogs)