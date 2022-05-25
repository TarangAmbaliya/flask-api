from datetime import timedelta
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
from app.models.user import User
from app.api.login import UserLogin


class SubmitOtp(Resource):

    def post(self):
        data = request.get_json()
        email = data['email']
        otp = data['otp']

        user = User.query.filter_by(email=email).first()
        if otp == UserLogin().get().create_otp:
            if 'remember_me' in data.keys():
                token = create_access_token(identity=user.name, fresh=False, expires_delta=False)
                return jsonify({'Auth Token': token})
            else:
                token = create_access_token(identity=user.name, fresh=True, expires_delta=(timedelta(days=1)))
                return jsonify({'Auth Token': token})
        else:
            return jsonify({'message': 'Incorrect OTP'})
