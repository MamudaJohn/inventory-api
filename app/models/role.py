from app import db
from flask_security import RoleMixin

class Role(db.Model, RoleMixin):
    __tablename__ = "role"

    id  = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique=True, nullable = False)
    description = db.Column(db.String, nullable=True)

    def to_dict(self):
        return {
            'id':self.id,
            'name' : self.name,
            'description': self.description
            }

    def add_role(self, name, description):
        if self.if_exist(name):
            return {"error": "The role already exists"}
        new_role = self(name=name, description=description)
        db.session.add(new_role)
        db.session.commit()

    def if_exist(self, name):
        if_exist = self.query.filter_by(name=name).first()
        if if_exist:
            return True
        return False

