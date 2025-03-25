from flask import render_template, request, Blueprint

from src.db import mysql

timelog_routes = Blueprint("timelog_routes", __name__)


@timelog_routes.route("/overview", methods=["GET", "POST"])
def show():
    conn = mysql.connect()
    cursor = conn.cursor()

    if request.method == "POST":
        delete_id = request.form.get("delete_id")
        if delete_id:
            cursor.execute(f"DELETE FROM timelog WHERE id = {delete_id}")
            conn.commit()

    cursor.execute("SELECT t.*, c.name, u.username FROM timelog as t JOIN category c ON t.category_id = c.id JOIN users u ON t.user_id = u.id ORDER BY t.date;")
    logs = cursor.fetchall()
    parsedLogs = [
        {
            "id": row[0],
            "timeFrom": str(row[1]),
            "date": row[2].strftime("%d.%m.%Y"),
            "timeTo": row[5],
            "category": row[6],
            "user": row[7]
        }
        for row in logs
    ]

    return render_template("overview.html", logs=parsedLogs)

@timelog_routes.route("/add",methods=["GET","POST"])
def add_new_timelog():
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category")
    categories =  cursor.fetchall()

    if request.method == "POST":
      catId = request.form.get("catSelect")
      date = request.form.get("date")
      timeFrom = request.form.get("timeFrom")
      timeTo = request.form.get("timeTo")
      print(catId,date,timeFrom, timeTo)
      cursor.execute(f"INSERT INTO timelog (timestampFrom, timestampTo, date,category_id, user_id) VALUES ('{timeFrom}','{timeTo}','{date}','{catId}','1')")
      conn.commit()
    return render_template("add_new_timelog.html",categories=categories)