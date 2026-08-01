from . import db
from . import app
from .models.user import User
from .models.role import Role
from flask import Blueprint
from flask_security import auth_required

bp = Blueprint('role', __name__ )

@auth_required
@bp.route("/add/role")
def addRole():
    roles = [role.to_dict() for role in Role.query.all()]

    return f"{roles}"


