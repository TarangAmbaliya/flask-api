from app.schema import UserSchema
from app.models import User, db
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource
from flask_jwt_extended import create_access_token


class UserRegister(Resource):

    def post(self):
        try:
            data = UserSchema().load(request.get_json())
        except ValidationError:
            return jsonify({'message': 'Partial input detected.'})
        name = data['name']
        email = data['email']
        password = data['password']

        if len(password) > 8:
            user = User(name, email, password)
            db.session.add(user)
        else:
            return jsonify({'message': 'Password length must be minimum 8 characters'})

        try:
            db.session.commit()
        except IntegrityError:
            return jsonify({'message': 'A account with this name or email already exist'})

        token = create_access_token(identity=name)
        return jsonify({'Auth Token': token})
