from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.models import db
from app.models.user import User
from app.schema.userSchema import UserSchema
from app.mail.sendEmail import Email


class UserRegister(Resource):

    def post(self):
        try:
            data = UserSchema().load(request.get_json())
        except ValidationError:
            return jsonify({'message': 'Partial input.'})
        name = data['name']
        email = data['email']
        password = data['password']

        if len(password) >= 8:
            user = User(name, email, password)
            db.session.add(user)
        else:
            return jsonify({'message': 'Password length must be minimum 8 characters.'})

        try:
            db.session.commit()
        except IntegrityError:
            return jsonify({'message': 'A account with this name or email already exists.'})

        token = create_access_token(identity=name)
        mail = list()
        mail.append(data['email'])
        Email(recipients=mail, name=data['name']).send_email()
        return jsonify({'Auth Token': token})
