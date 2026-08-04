from app.extensions import db
from app.models import StockLevel, StockMovement

class InsufficientStockError(Exception):
    pass

def record_stock_movement(
        product_id,
        warehouse_id,
        movement_type,
        quantity,
        performed_by,
        reference_id=None,
        reference_type=None,
        notes=None
        ):

    """
        Atomically records a stock movement and updates the corresponding
        stock level. Both writes succeed together or fail together.

        movement_type: 'in', 'out', 'transfer', 'adjustment'
        quantity: always a positive integer here; direction is determined
                by movement_type, not by the sign of quantity.
    """

    if quantity <= 0:
        raise ValueError("Quantity must be positive; directions is set by movement_type")

    stock_level = StockLevel.query.filter_by(product_id=product_id, warehouse_id=warehouse_id).first()

    if stock_level is None:
        stock_level = StockLevel(product_id=product_id, warehouse_id=warehouse_id, quantity=0)
        db.session.add(stock_level)

    if movement_type in ('in', 'adjustment_in'):
        stock_level.quantity += quantity
        signed_quantity = quantity

    elif movement_type in ("out", "adjustment_out"):
        if stock_level.quantity < quantity:
            raise InsufficientStockError(
                f"Cannot remove {quantity} units  - only {stock_level} is available"
            )
        stock_level.quantity -= quantity
        signed_quantity = -quantity

    else: 
        raise ValueError(f"Unknown movement type: {movement_type}")


    movement = StockMovement(
        product_id = product_id,
        warehouse_id = warehouse_id,
        movement_type = movement_type,
        quantity = signed_quantity,
        reference_type=reference_type,
        reference_id=reference_id,
        performed_by=performed_by,
        notes=notes
    )
    db.session.add(movement)
    db.session.commit()

    return stock_level, movement

