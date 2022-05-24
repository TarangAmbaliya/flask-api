from flask_restful import Api
from app.api.userRegister import UserRegister
from app.api.login import UserLogin
from app.api.passwordReset import ResetPassword
from app.api.refreshToken import GetRefreshToken

api = Api()

api.add_resource(UserRegister, "/api/register")
api.add_resource(UserLogin, "/api/login")
api.add_resource(ResetPassword, "/api/resetpass")
api.add_resource(GetRefreshToken, "/api/refresh")
