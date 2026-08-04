from app.extensions import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    company_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    billing_address = db.Column(db.Text, nullable=True)
    shipping_address = db.Column(db.Text, nullable=True)

    user = db.relationship("User", back_populates="customer_profile")

    def __repr__(self):
        return f"<Customer {self.company_name or self.user_id}>"

