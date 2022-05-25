from app.schema import ma
from app.models.role import Role
from marshmallow import EXCLUDE


class RoleSchema(ma.SQLAlchemyAutoSchemaMeta):
    class Meta:
        model = Role
        unknown = EXCLUDE
