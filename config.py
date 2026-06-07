import os
# For session cookies we need to set a secret key
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
