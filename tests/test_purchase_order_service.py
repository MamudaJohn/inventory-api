import pytest
from app.models import Product, Warehouse, Supplier, Role, User, PurchaseOrder, PurchaseOrderItem, StockLevel
from app.services.purchase_order_service import receive_purchase_order, InvalidStatusTransitionError


@pytest.fixture
def product(db):
    p = Product(sku="TEST-001", name="Test Widget", unit_price=10.00, cost_price=5.00)
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
def supplier(db):
    s = Supplier(name="Test Supplier Co")
    db.session.add(s)
    db.session.commit()
    return s


@pytest.fixture
def user(db):
    role = Role(name="warehouse_manager")
    db.session.add(role)
    db.session.commit()

    u = User(email="manager@sims.com", full_name="Test Manager", role_id=role.id)
    u.set_password("testpass123")
    db.session.add(u)
    db.session.commit()
    return u


def test_receiving_po_updates_status_and_stock(db, product, warehouse, supplier, user):
    po = PurchaseOrder(
        supplier_id=supplier.id, warehouse_id=warehouse.id,
        status="ordered", created_by=user.id
    )
    db.session.add(po)
    db.session.commit()

    item = PurchaseOrderItem(
        purchase_order_id=po.id, product_id=product.id,
        quantity=30, unit_cost=4.50
    )
    db.session.add(item)
    db.session.commit()

    received_po = receive_purchase_order(po.id, performed_by=user.id)

    assert received_po.status == "received"
    assert received_po.received_at is not None

    level = StockLevel.query.filter_by(product_id=product.id, warehouse_id=warehouse.id).first()
    assert level.quantity == 30


def test_cannot_receive_a_draft_po(db, product, warehouse, supplier, user):
    po = PurchaseOrder(
        supplier_id=supplier.id, warehouse_id=warehouse.id,
        status="draft", created_by=user.id
    )
    db.session.add(po)
    db.session.commit()

    with pytest.raises(InvalidStatusTransitionError):
        receive_purchase_order(po.id, performed_by=user.id)