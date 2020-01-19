from flask import Flask
from flask_graphql import GraphQLView
from flask_jwt import JWT
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .mixin import IdModel
from .permission import init_internal_permissions

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

    init_internal_permissions()

    from .api import schema  # isort:skip

    app.add_url_rule(
        "/", view_func=GraphQLView.as_view("graphql", schema=schema, batch=True)
    )

    return app
