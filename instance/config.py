import os
import datetime


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/usr')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY',
                                'c8acef83eebc388ff4657a65dae7a84bcfdcd7f9b99085c27136e7781e147ca7')
JWT_REFRESH_TOKEN_EXPIRES = os.environ.get('REFRESH_TOKEN_EXPIRY', datetime.timedelta(days=1))
JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('ACCESS_TOKEN_EXPIRY', datetime.timedelta(days=1))

MAIL_SERVER = 'smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = 'b982e751d200d2'
MAIL_PASSWORD = 'fac0e013df5431'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
