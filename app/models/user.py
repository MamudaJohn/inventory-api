from app import db
from .role import Role
from flask_security import UserMixin



user_role = db.Table(
    "userrole",
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), primary_key=True)    
)



class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy='dynamic'), lazy='selectin' )
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            "id" : self.id,
            'username' : self.username,
            "email" : self.email, 
            'role' : [sult.to_dict() for sult in self.roles]
        }

    def add_role_by_name(self, role:str):
        print("In the String section")
        existing_role = Role.query.filter_by(name = role).first()
        if existing_role and existing_role not in self.roles:
            self.roles.append(existing_role)
            print("Checking ....")
            return True
        print("The User already has this role", role)
        return False

    def add_role_by_name(self, role:list):
        print("In the list section")
        for rol in role:
            existing_role = Role.query.filter_by(name = rol).first()
            if existing_role:
                print("Checked if the role exists")
                if existing_role not in self.roles:
                    self.roles.append(existing_role)
                    print("Checking ....")
        return True
        # print("The User already has this role", role)
        # return False

    def remove_role_by_name(self, role):
        existing_role = Role.query.filter_by(name = role).first()
        if existing_role and existing_role in self.role:
            self.roles.remove(existing_role)
            return True
        return False

    @classmethod
    def add_user(cls, username, email, password, role, fs_uniquifier):
        if not cls.if_exists(username, email):
            new_user = cls(username = username, email = email, password = password, fs_uniquifier =fs_uniquifier)
            db.session.add(new_user)
            new_user.add_role_by_name(role)
            db.session.commit()
            return {"Message": "Successfully added a new user", "User": new_user.to_dict()}
        print("The user already exists")
        return {"Error": "User already exists"}

    def if_exists(username, email):
        existing_user = User.query.filter_by(username = username, email = email).first()
        if existing_user:
            return True
        return False






