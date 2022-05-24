from app.schema import ma
from app.models.user import User
from marshmallow import EXCLUDE


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True
        unknown = EXCLUDE
