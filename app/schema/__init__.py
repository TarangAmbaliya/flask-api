from flask_marshmallow import Marshmallow
from marshmallow import EXCLUDE
from app.models import User

ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True
        unknown = EXCLUDE
