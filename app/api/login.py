from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import check_password_hash
from app.models.user import User


class UserLogin(Resource):

    def get(self):
        data = request.get_json()
        name = data['name']
        password = data['password']
        remember_me = data['remember me']

        if not User.query.filter_by(name=name).one_or_none():
            return jsonify({'message': 'No User found.'})

        user = User.query.filter_by(name=name).one_or_none()
        if check_password_hash(user.password, password):
            if remember_me is True:
                token = create_access_token(identity=password, fresh=False, expires_delta=False)
                return jsonify({'Auth Token': token})
            else:
                token = create_access_token(identity=password, fresh=True, expires_delta=(timedelta(days=1)))
                return jsonify({'Auth Token': token})
        else:
            return jsonify({'message': 'Incorrect Password'})
