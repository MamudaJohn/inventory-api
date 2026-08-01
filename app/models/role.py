from app import db
from flask_security import RoleMixin

class Role(db.Model, RoleMixin):
    __tablename__ = "role"

    id  = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String, unique=True, nullable = False)
    description = db.Column(db.String, nullable=True)

    def to_dict(self):
        return {
            'id':self.id,
            'role' : self.role,
            'description': self.description
            }

    def add_role(self, role, description):
        if self.if_exist(role):
            return {"error": "The role already exists"}
        new_role = self(role=role, description=description)
        db.session.add(new_role)
        db.session.commit()

    def if_exist(self, role):
        if_exist = self.query.filter_by(role=role).first()
        if if_exist:
            return True
        return False

