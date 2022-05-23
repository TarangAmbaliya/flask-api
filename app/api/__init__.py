from flask_restful import Api
from app.api.userRegister import UserRegister
from app.api.login import UserLogin
from app.api.passwordReset import ResetPassword

api = Api()

api.add_resource(UserRegister, "/api/register")
api.add_resource(UserLogin, "/api/login")
api.add_resource(ResetPassword, "/api/resetpass")
