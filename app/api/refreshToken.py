from datetime import timedelta
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token
from flask import jsonify


class GetRefreshToken(Resource):

    @jwt_required(refresh=False)
    def get(self):
        return jsonify({'Refresh Token': create_refresh_token(identity=(get_jwt_identity()),
                                                              expires_delta=(timedelta(seconds=300)))})
