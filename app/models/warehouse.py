from app.extensions import db

class Warehouse(db.Model):
    __tablename__ = "warehouses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    manager = db.relationship("User", backref="managed_warehouses")

    def __repr__(self):
        return f"Warehouse {self.name}"

