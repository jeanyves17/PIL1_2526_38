from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO

db            = SQLAlchemy()
bcrypt        = Bcrypt()
login_manager = LoginManager()
socketio      = SocketIO()

def create_app(env="development"):
    flask_app = Flask(__name__)              # ← renommé en flask_app
    flask_app.config.from_object("config.Config")

    db.init_app(flask_app)
    bcrypt.init_app(flask_app)
    login_manager.init_app(flask_app)
    login_manager.login_view = "auth.login"
    socketio.init_app(flask_app, cors_allowed_origins="*", async_mode="threading")

    from app.routes.auth      import auth_bp
    from app.routes.profile   import profile_bp
    from app.routes.matching  import matching_bp
    from app.routes.messaging import messaging_bp

    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(profile_bp)
    flask_app.register_blueprint(matching_bp)
    flask_app.register_blueprint(messaging_bp)

    import app.services.messaging_service

    return flask_app                         # ← retourne bien l'instance Flask
