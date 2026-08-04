import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Get database URL from environment variable
    db_url = os.getenv("DATABASE_URL")
    
    # Render provides 'postgres://', but SQLAlchemy 1.4+ requires 'postgresql://'
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    
    db.init_app(app)
    
    return app
