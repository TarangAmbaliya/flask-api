from flask import request, jsonify, session
from flask_restful import Resource
# from flask_jwt_extended import create_access_token
# from datetime import timedelta
from werkzeug.security import check_password_hash
from app.models.user import User
from app.auth.twofactor import Otp
from app.mail.sendEmail import Email


class UserLogin(Resource):

    create_otp = Otp.generate_otp()

    @classmethod
    def get(cls):
        data = request.get_json()
        email = data['email']
        password = data['password']
        # remember_me = data['remember me']

        if not User.query.filter_by(email=email).one_or_none():
            return jsonify({'message': 'No User found.'})

        user = User.query.filter_by(email=email).one_or_none()
        if check_password_hash(user.password, password):
            mail = list()
            mail.append(data['email'])
            Email(template='otp.html', recipients=mail, otp=cls.create_otp).send_email()
