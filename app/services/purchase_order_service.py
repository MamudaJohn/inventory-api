from datetime import datetime, timezone
from app.extensions import db
from app.models import PurchaseOrder
from app.services.stock_service import record_stock_movement


class InvalidStatusTransitionError(Exception):
    pass


def receive_purchase_order(purchase_order_id, performed_by):
    """
    Transitions a PurchaseOrder to 'received' and records a stock movement
    for every line item, all in a single atomic transaction.
    """
    po = db.session.get(PurchaseOrder, purchase_order_id)

    if po is None:
        raise ValueError(f"Purchase order {purchase_order_id} not found")

    if po.status != "ordered":
        raise InvalidStatusTransitionError(
            f"Cannot receive a purchase order with status '{po.status}' — must be 'ordered'"
        )

    for item in po.items:
        record_stock_movement(
            product_id=item.product_id,
            warehouse_id=po.warehouse_id,
            movement_type="in",
            quantity=item.quantity,
            performed_by=performed_by,
            reference_type="purchase_order",
            reference_id=po.id,
            notes=f"Received from PO #{po.id}",
        )

    po.status = "received"
    po.received_at = datetime.now(timezone.utc)
    db.session.commit()

    return po