from flask import Flask

from src.auth_routes import auth_routes
from src.main_routes import main_routes
from src.tickets_routes import tickets_routes


app = app = Flask(__name__)

app.register_blueprint(auth_routes)
app.register_blueprint(main_routes)
app.register_blueprint(tickets_routes)
