import pytest
from app.models import Product, Warehouse, Role, User
from app.services.stock_service import record_stock_movement, InsufficientStockError
from app.extensions import db as _db


@pytest.fixture
def product(db):
    p = Product(
        sku="Test-001",
        name="Test Widget",
        unit_price= 10.00,
        cost_price = 5.00
    )
    db.session.add(p)
    db.session.commit()
    return p

@pytest.fixture
def warehouse(db):
    w = Warehouse(name="Main Warehouse")
    db.session.add(w)
    db.session.commit()
    return w

@pytest.fixture
def user(db):
    role = Role(name="warehouse manager")
    db.session.add(role)
    db.session.commit()

    u = User(email="manager@sims.com", full_name="Test Manager", role_id=role.id)
    u.set_password("testpass123")
    db.session.add(u)
    db.session.commit()
    return u


def test_stock_in_increases_level(db, product, warehouse, user):
    level, movement = record_stock_movement(
        product_id=product.id, warehouse_id=warehouse.id, movement_type="in",
        quantity=50, performed_by=user.id, reference_type="manual"
    )
    assert level.quantity == 50
    assert movement.quantity == 50

def test_stock_out_decrease_level(db, product, warehouse, user):
    record_stock_movement(
        product_id=product.id, warehouse_id=warehouse.id, movement_type="in",
        quantity=50, performed_by=user.id
    )
    level, movement = record_stock_movement(
        product_id=product.id, warehouse_id=warehouse.id,
        movement_type="out", quantity=20, performed_by=user.id
    )
    assert level.quantity == 30
    assert movement.quantity == -20

def test_cannot_remove_more_than_available(db, product, warehouse, user):
    record_stock_movement(
        product_id=product.id, warehouse_id=warehouse.id,
        movement_type="in", quantity=10, performed_by=user.id
    )
    with pytest.raises(InsufficientStockError):
        record_stock_movement(
            product_id=product.id, warehouse_id=warehouse.id,
            movement_type="out", quantity=999, performed_by=user.id
        )

def test_movements_sum_matches_stock_level(db, product, warehouse, user):
    """The core invariant: SUM(stock_movements.quantity) == stock_levels.quantity"""
    from sqlalchemy import func
    from app.models import StockMovement, StockLevel

    record_stock_movement(
        product_id=product.id, warehouse_id=warehouse.id, movement_type="in", quantity=50, performed_by=user.id
    )
    record_stock_movement(
        product_id=product.id, warehouse_id=warehouse.id, movement_type="out", quantity=20, performed_by=user.id
    )
    record_stock_movement(
        product_id=product.id, warehouse_id=warehouse.id, movement_type="in", quantity=5, performed_by=user.id
    )

    total_moved = db.session.query(func.sum(StockMovement.quantity)).filter_by(product_id=product.id, warehouse_id=warehouse.id).scalar()
    current_level = StockLevel.query.filter_by(product_id=product.id, warehouse_id=warehouse.id).first()

    assert total_moved == current_level.quantity


