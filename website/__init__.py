from flask import Flask
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from .models import db, User
from .utils import createAdminUser
import os

csrf = CSRFProtect()
limiter = Limiter(get_remote_address)

def create_app():
    app = Flask(__name__, static_folder='static')

    # Your config...
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocobell.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'CHANGE_THIS_TO_A_RANDOM_KEY'
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/sounds')

    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.authLogin'
    login_manager.login_message_category = 'info'

    from .user import user
    from .auth import auth
    app.register_blueprint(user)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()
        createAdminUser()

    return app
