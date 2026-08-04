from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    # Import models AFTER db.init_app so they register against the
    # same SQLAlchemy instance, but BEFORE db.create_all() runs.
    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    # Blueprints
    from app.auth import auth
    from app.dashboard import dashboard
    from app.profile import profile
    from app.travel import travel
    from app.ai import ai

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(profile)
    app.register_blueprint(travel)
    app.register_blueprint(ai)

    with app.app_context():
        db.create_all()

    return app
