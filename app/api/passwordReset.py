from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from app.models import db
from app.models.user import User
from app.schema.userSchema import UserSchema


class ResetPassword(Resource):

    @jwt_required(refresh=True)
    def patch(self):
        name = get_jwt_identity()
        data = UserSchema().load(request.get_json(), partial=True)
        if 'password' not in data.keys():
            return jsonify({'message': 'No new password provided'})
        else:
            user = User.query.filter_by(name=name).first()

        user.password = generate_password_hash(data['password'])
        db.session.commit()

        return jsonify({'message': 'Password reset successful'})
