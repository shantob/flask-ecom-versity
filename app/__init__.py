from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'info'

    from app.models import Admin

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Register Blueprints
    from app.routes import main_bp, cart_bp
    from app.admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
