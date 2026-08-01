from . import db
from . import app
from .models.user import User
from .models.role import Role
from flask import Blueprint

bp = Blueprint('role', __name__ )

@bp.route("/add/role")
def addRole():
    roles = [role.to_dict() for role in Role.query.all()]

    return f"{roles}"

