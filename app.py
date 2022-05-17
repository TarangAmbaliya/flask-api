import os
from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'c8acef83eebc388ff4657a65dae7a84bcfdcd7f9b99085c27136e7781e147ca7'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Username cannot be empty.')
parser.add_argument('email', type=str, required=False, help='Email is not mandatory.')
parser.add_argument('password', type=str, required=True, help='Password cannot be empty.')


class User(db.Model):
    __tablename__ = 'UserData'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password, "sha256")


class UserSchema(ma.Schema):
    fields = ('id', 'username', 'email', 'password')
    model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserRegister(Resource):

    def post(self):
        data = parser.parse_args()
        name = data['name']
        email = data['email']
        password = data['password']

        # user = User.query.filter_by(name=name).one_or_none()
        # user_email = User.query.filter_by(email=email).one_or_none()

        # if not user or not user_email:
            # return jsonify({'message': 'Username or email already exists.'})
        #
        # if len(name) or len(password) == 0:
        #     return jsonify({'message': 'Invalid Data'})

        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=name)
        return jsonify(token)


class UserGetToken(Resource):

    def get(self):
        data = parser.parse_args()
        name = data['name']
        password = data['password']

        if not User.query.filter_by(name=name).one_or_none():
            return jsonify({'message': 'No User found.'})

        user = User.query.filter_by(name=name).one_or_more()
        if check_password_hash(user.password_hash, password):
            token = create_access_token(identity=name)
            return jsonify(token)
        else:
            return jsonify({'message': 'Incorrect Password'})


class UserUD(Resource):

    @jwt_required()
    def patch(self):
        data = parser.parse_args()
        name = data['name']
        email = data['email']
        password = data['password']

        if len(name) > 0 or len(email) > 0 or len(password):
            user = User.query.filter_by(name=name).one_or_none()
            if name in data.keys():
                user.name = name
            if email in data.keys():
                user.email = email
            if password in data.keys():
                user.password_hash = generate_password_hash(password)
            db.session.commit()
        else:
            return jsonify({'message': 'No data provided to update.'})

    @jwt_required()
    def delete(self):
        data = parser.parse_args()
        name = data['name']
        email = data['email']

        if len(name) > 0 or len(email) > 0:
            user = User.query.filter_by(name).first()
            db.session.delete(user)
            db.session.commit()


db.create_all()
api.add_resource(UserRegister, "/api/register")
api.add_resource(UserGetToken, "/api/gettoken")
api.add_resource(UserUD, "/api/update")
if __name__ == '__main__':
    app.run(Debug=True)
