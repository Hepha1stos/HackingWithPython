# src/__init__.py

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.db import mysql

# 1) Flask-App erstellen
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST']     = 'localhost'
app.config['MYSQL_DATABASE_USER']     = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB']       = 'local'
app.secret_key = "DEIN_SUPER_GEHEIMER_STRING"

# 2) Limiter-Instanz erzeugen und direkt an app binden
limiter = Limiter(
    key_func=get_remote_address,  # Limitiert standardmäßig pro IP-Adresse
    storage_uri="memory://"       # In-Memory-Backend (für Tests/Entwicklung)
)
limiter.init_app(app)

# 3) MySQL-Extension initialisieren
mysql.init_app(app)

# 4) Blueprints importieren und registrieren
#    Wichtig: limiter muss VOR auth_routes importiert werden, weil auth_routes "from src import limiter" erwartet
from src.auth_routes import auth_routes
from src.main_routes import main_routes
from src.timelog_routes import timelog_routes

app.register_blueprint(auth_routes)
app.register_blueprint(main_routes)
app.register_blueprint(timelog_routes)
