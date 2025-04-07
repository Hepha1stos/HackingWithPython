from flask import render_template, request, Blueprint, redirect

from src.db import mysql
from funcs.cookies import checkCookie
timelog_routes = Blueprint("timelog_routes", __name__)


@timelog_routes.route("/overview", methods=["GET", "POST"])
def show():
    cookie = checkCookie()
    if not cookie:
        return redirect("login")

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
            "date": row[3].strftime("%d.%m.%Y"),
            "timeTo": row[2],
            "category": row[6],
            "user": row[7]
        }
        for row in logs
    ]

    return render_template("overview.html", logs=parsedLogs, cookie=cookie)

@timelog_routes.route("/add",methods=["GET","POST"])
def add_new_timelog():
    cookie = checkCookie()
    if not cookie:
        return redirect("login")
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category")
    categories =  cursor.fetchall()

    if request.method == "POST":
        
      username = request.cookies.get("name")
      catId = request.form.get("catSelect")
      date = request.form.get("date")
      timeFrom = request.form.get("timeFrom")
      timeTo = request.form.get("timeTo")

      print(f"--> INSERT timelog: category_id:{catId}, date:{date}, timeFrom:{timeFrom}, timeTo:{timeTo} for user {username}")
    
      cursor.execute(f"INSERT INTO timelog (timestampFrom, timestampTo, date,category_id, user_id) VALUES ('{timeFrom}','{timeTo}','{date}','{catId}',(SELECT id from users where username = '{username}'))")
      conn.commit()
      return redirect("/overview")
    return render_template("add_new_timelog.html",categories=categories, cookie=cookie)


@timelog_routes.route("/edit/<id>", methods=["GET","POST"])
def edit_timelog(id):
    
    cookie = checkCookie()
    if not cookie:
        return redirect("login")
    
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(f"SELECT timeStampFrom,timeStampTo,date,category_id,u.username from timelog JOIN users u ON timelog.user_id = u.id where timelog.id = '{id}'")
    log = cursor.fetchone()
    colums = [desc[0] for desc in cursor.description]
    log_dict = dict(zip(colums, log))

    cursor.execute("SELECT * from category")
    categories = cursor.fetchall()
 
    if request.method == "POST":

        catId = request.form.get("catSelect")
        date = request.form.get("date")
        timeFrom = request.form.get("timeStampFrom")
        timeTo = request.form.get("timeStampTo")
        
        print(f"--> GOT for EDIT: TimeTo:{timeTo},TimeFrom:{timeFrom},Date:{date},ID:{catId}")
        
        conn = mysql.connect()
        cursor = conn.cursor()

        print(f"--> Update timelog with ID {id}: category_id:{catId}, date:{date}, timeFrom:{timeFrom}, timeTo:{timeTo}")

        cursor.execute(f"UPDATE timelog SET category_id='{catId}', date='{date}', timeStampFrom='{timeFrom}', timeStampTo='{timeTo}' WHERE id='{id}'")
        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/overview")
  

    return render_template("edit.html",log=log_dict,categories=categories, cookie=cookie)


@timelog_routes.route("/delete/<id>")
def delete_timelog(id):
     
    cookie = checkCookie()
    if not cookie:
        return redirect("login")
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    print(f"--> DELETE timelog with ID {id}")

    cursor.execute(f"DELETE from timelog where id = '{id}'")
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/overview")