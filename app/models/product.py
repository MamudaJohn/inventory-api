from app.extensions import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)

    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    cost_price = db.Column(db.Numeric(10, 2), nullable=False)
    reorder_threshold = db.Column(db.Integer, nullable=False, default=10)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    category = db.relationship("Category", backref="products")
    supplier = db.relationship("Supplier", backref="products")

    def __repr__(self):
        return f"Product {self.sku} {self.name}"