from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import check_password_hash
from app.models.user import User
from app.auth.twofactor import Otp
from app.mail.sendEmail import Email


class UserLogin(Resource):

    otp = Otp()

    @classmethod
    def get(cls):
        data = request.get_json()
        email = data['email']
        password = data['password']

        if not User.query.filter_by(email=email).one_or_none():
            return jsonify({'message': 'No User found.'})

        user = User.query.filter_by(email=email).one_or_none()
        if check_password_hash(user.password, password):
            mail = list()
            mail.append(data['email'])
            Email(template='otp.html', recipients=mail, otp=cls.otp.generate_otp(user.email)).send_email()
            return jsonify({'message': 'Otp sent successfully.'})
        else:
            return jsonify({'message': 'Incorrect Password'})
