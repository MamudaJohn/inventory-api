import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_fallback_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev_jwt_fallback_key")

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")