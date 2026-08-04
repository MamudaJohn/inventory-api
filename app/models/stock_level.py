from app.extensions import db

class StockLevel(db.Model):
    __tablename__ = "stock_levels"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    product = db.relationship("Product", backref="stock_levels")
    warehouse = db.relationship("Warehouse", backref="stock_levels") 

    __table_args__ = (
        db.UniqueConstraint("product_id", "warehouse_id", name="uq_product_warehouse"),
        db.CheckConstraint("quantity >= 0", name="ck_stock_quantity_non_negative"),
    )


    def __repr__(self):
        return f"Stock Level product = {self.product_id}, warehouse = {self.warehouse_id} and quantity = {self.quantity}"
