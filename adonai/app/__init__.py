from flask import Flask
from flask_jwt import JWT
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .mixin import IdModel

db = SQLAlchemy(model_class=IdModel)
migrate = Migrate(directory=Config.MIGRATIONS_DIR)
jwt = JWT()

from .models import *  # isort:skip
from .resources import *  # isort:skip
from .auth import *  # isort:skip


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    return app
