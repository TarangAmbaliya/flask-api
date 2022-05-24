from app.models.user import db


class Role(db.model):

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, role):
        self.role = role
