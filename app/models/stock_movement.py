from app.extensions import db
from datetime import datetime

class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)

    movement_type = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    reference_type = db.Column(db.String(30), nullable=True)
    reference_id = db.Column(db.Integer, nullable=True)

    performed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    notes =db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow() , nullable=False)

    product = db.relationship("Product", backref="stock_movements")
    warehouse = db.relationship("Warehouse", backref="stock_movements")
    user = db.relationship("User", backref="stock_movements")


    __table_args__ = (
        db.CheckConstraint("quantity != 0", name="ck_movement_quantity_nonzero"),
    )


    def __repr__(self):
        return f"Stock Movement : {self.movement_type}, quantity : {self.quantity} and product : {self.product_id}"

