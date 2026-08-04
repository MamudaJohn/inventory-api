import pytest
from app.extensions import db as _db
from app.config import TestConfig
from app import create_app

@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    return app


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

