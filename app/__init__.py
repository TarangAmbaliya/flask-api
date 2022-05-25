from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    from app.models import db
    db.init_app(app)

    from app.schema import ma
    ma.init_app(app)

    from app.api import api
    api.init_app(app)

    from app.auth import jwt
    jwt.init_app(app)

    from app.mail import mail
    mail.init_app(app)

    @app.before_first_request
    def table_create():
        db.create_all()

    return app
