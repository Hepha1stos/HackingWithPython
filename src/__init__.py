# src/__init__.py

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.db import mysql


app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST']     = 'localhost'
app.config['MYSQL_DATABASE_USER']     = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB']       = 'local'
app.secret_key = "DESDKJHSDFK_UJFDHGI/%Z$I/ZRO(I/GUKFHBGKUDFRHhfughufhguh54h894hg895hgukfhgkdufhgp98e75)"


limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://"       
)
limiter.init_app(app)


mysql.init_app(app)



from src.auth_routes import auth_routes
from src.main_routes import main_routes
from src.timelog_routes import timelog_routes

app.register_blueprint(auth_routes)
app.register_blueprint(main_routes)
app.register_blueprint(timelog_routes)
