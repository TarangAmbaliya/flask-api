from app.models import User
from app.schema import UserSchema
from app.models import db, generate_password_hash
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource


@jwt_required(fresh=True)
class ResetPassword(Resource):
    def patch(self):
        data = UserSchema().load(request.get_json(), partial=True)
        name = data['name']
        email = data['email']
        password = data['password']

        if len(name) > 0 or len(email) > 0 or len(password) > 8:
            user = User.query.filter_by(name=name).one_or_none()
            if password not in data.keys():
                return jsonify({'message': 'No password provided to reset.'})
            elif password == user.password:
                return jsonify({'message': 'The password cannot be as same as the previous password.'})
            else:
                user.password = generate_password_hash(password)
                db.session.commit()
                return jsonify({'message': 'Password reset successfull.'})
        else:
            return jsonify({'message': 'Invalid Password.'})
