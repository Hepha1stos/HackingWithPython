from flask import render_template, request, Blueprint



tickets_routes = Blueprint("tickets_routes", __name__)

@tickets_routes.route("/tickets")
def tickets_page():
    items= [{"id":1,"priority":2,"username":"Mark","title":"something broken"},
            {"id":2,"priority":4,"username":"Luke","title":"something working"},
            {"id":3,"priority":1,"username":"Thomas","title":"something waiting"}
            ]
    return render_template("tickets.html",items=items)