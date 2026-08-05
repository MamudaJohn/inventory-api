from app.extensions import db
from datetime import datetime, timezone

class PurchaseOrder(db.Model):
    __tablename__ = "purchase_orders"

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="draft")
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    received_at = db.Column(db.DateTime, nullable=True)

    supplier = db.relationship("Supplier", backref="purchase_orders")
    warehouse = db.relationship("Warehouse", backref="purchase_orders")
    creator = db.relationship("User", backref="purchase_orders_created")
    items = db.relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('draft', 'ordered', 'received', 'cancelled')", name="ck_purchase_order_status"
        ),
    )

    def __repr__(self):
        return f"<PurchaseOrder {self.id} - {self.status}>"


