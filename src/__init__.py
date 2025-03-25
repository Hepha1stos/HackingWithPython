from flask import Flask
from src.db import mysql
from src.auth_routes import auth_routes
from src.main_routes import main_routes
from src.tickets_routes import tickets_routes

app = Flask(__name__)

# Konfig
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'local'

# Init Extensions
mysql.init_app(app)

# Blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(main_routes)
app.register_blueprint(tickets_routes)
