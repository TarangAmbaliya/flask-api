import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'c8acef83eebc388ff4657a65dae7a84bcfdcd7f9b99085c27136e7781e147ca7'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)


class User(db.Model):

    __tablename__ = 'UserData'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password, "sha256")

    def __repr__(self):
        return jsonify({"User": self.name})


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserRegister(Resource):

    def post(self):
        data = user_schema.load(request.get_json())
        name = data['name']
        email = data['email']
        password = data['password']

        if not name or not email or not password:
            return jsonify({'message': 'Invalid Data'})

        user = User(name, email, password)
        db.session.add(user)

        try:
            db.session.commit()
        except exc.IntegrityError:
            return {'message': 'A account with this name or email already exist'}, 403

        token = create_access_token(identity=name, expires_delta=False)
        return jsonify({'Auth Token': token})


class UserGetToken(Resource):

    def get(self):
        data = user_schema.load(request.get_json(), partial=True)
        name = data['name']
        password = data['password']

        if not User.query.filter_by(name=name).one_or_none():
            return jsonify({'message': 'No User found.'})

        user = User.query.filter_by(name=name).one_or_none()
        if check_password_hash(user.password, password):
            token = create_access_token(identity=name)
            return jsonify(token)
        else:
            return jsonify({'message': 'Incorrect Password'})


class UserUD(Resource):

    @jwt_required()
    def patch(self):
        data = user_schema.load(request.get_json())
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
                user.password = generate_password_hash(password)
            db.session.commit()
        else:
            return jsonify({'message': 'No data provided to update.'})

    @jwt_required()
    def delete(self):
        data = request.get_json()
        data = user_schema.load(data)
        name = data['name']
        email = data['email']

        if len(name) > 0 or len(email) > 0:
            user = User.query.filter_by(name).first()
            db.session.delete(user)
            db.session.commit()


class GetAllUsers(Resource):

    @jwt_required()
    def get(self):
        data = user_schema.load(request.get_json(), partial=True)
        get_user_list = User.query.with_entities(User.name, User.email).filter_by(name=data['name'])
        return users_schema.dump(get_user_list, many=True)


db.create_all()
api.add_resource(UserRegister, "/api/register")
api.add_resource(UserGetToken, "/api/gettoken")
api.add_resource(UserUD, "/api/update")
api.add_resource(GetAllUsers, '/api/getallusers')

if __name__ == '__main__':
    app.run(Debug=True)
