import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'c8acef83eebc388ff4657a65dae7a84bcfdcd7f9b99085c27136e7781e147ca7'
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = os.environ.get('ACCESS_TOKEN_EXPIRY')
    app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = 'b982e751d200d2'
    app.config['MAIL_PASSWORD'] = 'fac0e013df5431'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

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
