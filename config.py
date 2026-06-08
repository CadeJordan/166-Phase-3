import os

# For session cookies we need to set a secret key
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "cjord019_phase3_DB")
DB_USER = os.environ.get("DB_USER", "cjord019")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")