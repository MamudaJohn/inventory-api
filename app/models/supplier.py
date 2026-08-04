from app.extensions import db

class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact_email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    address = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Supplier: {self.name}"




