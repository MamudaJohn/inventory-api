from flask import Blueprint, request, jsonify
from app.services.stock_service import record_stock_movement, InsufficientStockError
from app.utils.decorators import roles_required

inventory_bp = Blueprint("inventory", __name__, url_prefix="/api/inventory")


@inventory_bp.route("/stock-movements", methods=['POST'])
@roles_required("warehouse_manager", 'super_admin')
def create_stock_movement():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No input data provided"
        }), 400

    required_fields = ["product_id", "warehouse_id", "movement_type", "quantity"]
    missing = [f for f in required_fields if f not in data ]
    if missing:
        return jsonify({
            "Error": f"Missing fields: {", ".join(missing)}"
        }), 400

    from flask_jwt_extended import get_jwt_identity
    performed_by = int(get_jwt_identity())

    try:
        stock_level, movement = record_stock_movement(
            product_id=data["product_id"],
            warehouse_id=data["warehouse_id"],
            movement_type=data["movement_type"],
            quantity=data["quantity"],
            performed_by=performed_by,
            reference_type=data.get("reference_type"),
            reference_id=data.get("reference_id"),
            notes=data.get("notes")
        )
    except InsufficientStockError as e:
        return jsonify({"Error": str(e)}), 409
    except ValueError as e:
        return jsonify({"Error": str(e)}), 400

    return jsonify({
        "message": "Stock movement recorded",
        "stock_level": {
            "product_id": stock_level.product_id,
            "warehouse_id": stock_level.warehouse_id,
            "quantity": stock_level.quantity
        },
        "movement": {
            "id": movement.id,
            "movement_type": movement.movement_type,
            "quantity": movement.quantity,
            "created_at": movement.created_at.isoformat()
        }
    }), 201


