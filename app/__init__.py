from flask import Flask
from .config import Config
from .extensions import db, migrate, bcrypt, jwt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    with app.app_context():
        from app import models
        from app.blueprints.auth import auth_bp
        from app.blueprints.inventory import inventory_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(inventory_bp)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)


    # Blueprint will go in here
    # Blueprint registration will go in here
    

    
    return app
