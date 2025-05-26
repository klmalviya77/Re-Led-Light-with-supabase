import os
import logging
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///reled.db")
# Fix for incorrect database URL format
if database_url.startswith("https://"):
    print("Warning: DATABASE_URL appears to be an HTTPS URL, using SQLite instead")
    database_url = "sqlite:///reled.db"
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Make datetime available in templates
@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Create all tables
    db.create_all()
    
    # Initialize sample data if tables are empty
    from models import Product, Category
    if not Product.query.first():
        models.init_sample_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
