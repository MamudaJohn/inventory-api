from flask import request, jsonify, Blueprint
from app.extensions import db
from app.models import User, Role
from app.utils.decorators import roles_required
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({
            "Error": "No input data provided"
        }), 400

    required_fields = ["email", "password", "full_name", "role_name"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({
            "Error": f"Missing fields: {', '.join(missing)}"
        }), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            "Error": f"Email already registered"
        }), 409

    role = Role.query.filter_by(name=data['role_name']).first()
    if not role:
        return jsonify({
            "error": f"Role '{data['role_name']}' does not exist"
        }), 400

    user = User(
        email = data['email'],
        full_name=data['full_name'],
        role_id=role.id,
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "Message": "User registered successfully",
        "user_id": user.id
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({
            "Error": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({
            "Error": "Invalid email or password"
        }), 401

    if not user.is_active:
        return jsonify({
            "Error": "Account is disabled"
        }), 403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role.name}
    )
    print(access_token)

    return jsonify({
        "access_token": access_token,
        "role": user.role.name 
    }), 200

@auth_bp.route('/me', methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    claims = get_jwt()
    return jsonify({
        "user_id": user_id,
        "role": claims.get('role')
    })

@auth_bp.route('/admin', methods=["GET"])
@roles_required('super_admin')
def admin():
    return jsonify({
        "Message": "Welcome our most prestige guest"
    }), 200
