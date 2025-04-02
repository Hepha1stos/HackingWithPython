from flask import render_template, request, Blueprint


main_routes = Blueprint("main_routes",__name__)

@main_routes.route("/")
def homepage():
    cookie = request.cookies.get('name')
    print(cookie)
    return render_template('home.html', cookie=cookie)



