from datetime import timedelta
from app.api.userRegister import Resource
from app.api.passwordReset import jwt_required, get_jwt_identity
from flask_jwt_extended import create_refresh_token
from app.api.userRegister import jsonify


@jwt_required()
class GetRefreshToken(Resource):
    def get(self):
        return jsonify(create_refresh_token(identity=(get_jwt_identity()),
                                            expires_delta=(timedelta(seconds=600))))
