from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='static')

    from .user import user
    app.register_blueprint(user)

    return app
