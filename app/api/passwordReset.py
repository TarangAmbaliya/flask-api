from app.models.user import User, db, generate_password_hash
from app.schema.userSchema import UserSchema
from app.api.login import Resource
from app.api.userRegister import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required(fresh=True)
class ResetPassword(Resource):
    def patch(self):
        name = get_jwt_identity()
        data = UserSchema().load(request.get_json())
        if 'password' not in data.keys():
            return jsonify({'message': 'No new password provided'})
        else:
            user = User.Query.filter_by(name=name).first()

        user.password = generate_password_hash(data['password'])
        db.session.commit()

        return jsonify({'message': 'Password reset successful'})
