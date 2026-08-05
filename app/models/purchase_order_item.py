from app.extensions import db

class PurchaseOrderItem(db.Model):
    __tablename__ = "purchase_order_items"

    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey("purchase_orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Numeric(10, 2), nullable=False)

    purchase_order = db.relationship("PurchaseOrder", back_populates="items")
    product = db.relationship("Product", backref="purchase_order_items")

    __table_args__ = (
        db.CheckConstraint("quantity > 0", name="ck_po_item_quantity_positive"),
    )

    def __repr__(self):
        return f"<PurchaseOrderItem product={self.product_id} qty={self.quantity}>"
    
