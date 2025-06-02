from flask import render_template, request, Blueprint, redirect, session, url_for
from src.db import mysql

timelog_routes = Blueprint("timelog_routes", __name__)

def check_session():
    """
    Gibt user_id zurück, wenn der User eingeloggt ist, sonst None.
    """
    return session.get("user_id")


@timelog_routes.route("/overview", methods=["GET", "POST"])
def show():
    user_id = check_session()
    if not user_id:
        return redirect(url_for("auth_routes.user_login"))

    conn = mysql.connect()
    cursor = conn.cursor()

    # Wenn gelöscht werden soll
    if request.method == "POST":
        delete_id = request.form.get("delete_id")
        if delete_id:
            cursor.execute(
                "DELETE FROM timelog WHERE id = %s AND user_id = %s",
                (delete_id, user_id)
            )
            conn.commit()

    # Alle Einträge abrufen (inkl. Von/Bis)
    cursor.execute(
        "SELECT t.id, "
        "       t.timestampFrom, "
        "       t.timestampTo, "
        "       t.date, "
        "       t.description, "
        "       c.name      AS category_name, "
        "       u.username AS username "
        "FROM timelog AS t "
        "JOIN category AS c ON t.category_id = c.id "
        "JOIN users    AS u ON t.user_id     = u.id "
        "ORDER BY t.date DESC;"
    )
    rows = cursor.fetchall()

    parsedLogs = []
    for row in rows:
        # row[1] und row[2] sind datetime.time oder datetime.timedelta
        # Wir formatieren immer in "HH:MM"
        if row[1] is not None:
            try:
                time_from = row[1].strftime("%H:%M")
            except AttributeError:
                total_seconds = row[1].total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                time_from = f"{hours:02d}:{minutes:02d}"
        else:
            time_from = ""

        if row[2] is not None:
            try:
                time_to = row[2].strftime("%H:%M")
            except AttributeError:
                total_seconds = row[2].total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                time_to = f"{hours:02d}:{minutes:02d}"
        else:
            time_to = ""

        date_str = row[3].strftime("%d.%m.%Y") if row[3] is not None else ""

        parsedLogs.append({
            "id":          row[0],
            "timeFrom":    time_from,
            "timeTo":      time_to,
            "date":        date_str,
            "description": row[4] or "",
            "category":    row[5] or "",
            "user":        row[6] or "",
            "username":    row[6] or ""
        })

    cursor.close()
    conn.close()
    return render_template("overview.html", logs=parsedLogs)


@timelog_routes.route("/add", methods=["GET", "POST"])
def add_new_timelog():
    user_id = check_session()
    if not user_id:
        return redirect(url_for("auth_routes.user_login"))

    conn = mysql.connect()
    cursor = conn.cursor()

    # Kategorien für das Formular laden
    cursor.execute("SELECT id, name FROM category")
    categories = cursor.fetchall()

    if request.method == "POST":
        description = request.form.get("description") or ""
        date        = request.form.get("date") or ""
        timeFrom    = request.form.get("timeFrom") or ""
        timeTo      = request.form.get("timeTo") or ""
        category_id = request.form.get("category_id") or 1

        cursor.execute(
            """
            INSERT INTO timelog (
                timestampFrom,
                timestampTo,
                date,
                description,
                user_id,
                category_id
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (timeFrom, timeTo, date, description, user_id, category_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/overview")

    cursor.close()
    conn.close()
    return render_template("add_new_timelog.html", categories=categories)


@timelog_routes.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_timelog(id):
    user_id = check_session()
    if not user_id:
        return redirect(url_for("auth_routes.user_login"))

    conn = mysql.connect()
    cursor = conn.cursor()

    # 1. Bestehenden Eintrag holen (inkl. Username)
    cursor.execute(
        """
        SELECT t.timestampFrom,
               t.timestampTo,
               t.date,
               t.description,
               t.category_id,
               u.username
        FROM timelog AS t
        JOIN users AS u ON t.user_id = u.id
        WHERE t.id = %s AND t.user_id = %s
        """,
        (id, user_id)
    )
    row = cursor.fetchone()  # Tupel oder None

    # 2. Kategorien laden
    cursor.execute("SELECT id, name FROM category")
    categories = cursor.fetchall()

    if not row:
        cursor.close()
        conn.close()
        return redirect(url_for("timelog_routes.show"))

    # 3. "Von"/"Bis" in "HH:MM" umwandeln
    # timeFrom
    if row[0] is not None:
        try:
            time_from_str = row[0].strftime("%H:%M")
        except AttributeError:
            total_seconds = row[0].total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            time_from_str = f"{hours:02d}:{minutes:02d}"
    else:
        time_from_str = ""

    # timeTo
    if row[1] is not None:
        try:
            time_to_str = row[1].strftime("%H:%M")
        except AttributeError:
            total_seconds = row[1].total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            time_to_str = f"{hours:02d}:{minutes:02d}"
    else:
        time_to_str = ""

    # Datum im Format "YYYY-MM-DD"
    try:
        date_str = row[2].strftime("%Y-%m-%d")
    except Exception:
        date_str = ""

    log_dict = {
        "timeFrom":    time_from_str,     # input name="timeFrom"
        "timeTo":      time_to_str,       # input name="timeTo"
        "date":        date_str,          # input name="date"
        "description": row[3] or "",      # input name="description"
        "category_id": row[4],            # input name="category_id"
        "username":    row[5] or ""       # für Anzeigezwecke
    }

    # 4. POST: Änderungen speichern
    if request.method == "POST":
        new_date        = request.form.get("date") or log_dict["date"]
        new_timeFrom    = request.form.get("timeFrom") or log_dict["timeFrom"]
        new_timeTo      = request.form.get("timeTo") or log_dict["timeTo"]
        new_description = request.form.get("description") or log_dict["description"]
        new_category    = request.form.get("category_id") or log_dict["category_id"]

        cursor.execute(
            """
            UPDATE timelog
            SET timestampFrom = %s,
                timestampTo   = %s,
                date          = %s,
                description   = %s,
                category_id   = %s
            WHERE id = %s AND user_id = %s
            """,
            (new_timeFrom, new_timeTo, new_date, new_description, new_category, id, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/overview")

    cursor.close()
    conn.close()
    # 5. Rendern mit den korrekt formatierten Werten
    return render_template("edit.html", log=log_dict, categories=categories)


@timelog_routes.route("/delete/<int:id>")
def delete_timelog(id):
    user_id = check_session()
    if not user_id:
        return redirect(url_for("auth_routes.user_login"))

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM timelog WHERE id = %s AND user_id = %s",
        (id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/overview")
