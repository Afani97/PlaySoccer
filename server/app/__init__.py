import sentry_sdk
from flask import Flask, request, session, jsonify, g
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from config import Config, ProductionConfig

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()


def create_app(config_class=Config):
    app = Flask(__name__)
    if app.env == "production":
        app.config.from_object(ProductionConfig)
        sentry_sdk.init(
            dsn="DNS_FROM_SENTRY",
            integrations=[FlaskIntegration(), SqlalchemyIntegration()]
        )
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials=True,
                  origins=app.config["ORIGIN"],
                  allow_headers=["X-Requested-With", "Content-Type", "Accept", "Origin", "Access-Control-Request-Method"])

    from app.routes import auth
    app.register_blueprint(auth.auth_bp, url_prefix='/api/auth')

    from app.routes import profile
    app.register_blueprint(profile.profile_bp, url_prefix='/api/profile')

    from app.routes import events
    app.register_blueprint(events.events_bp, url_prefix='/api/events')

    from app.routes import current
    app.register_blueprint(current.current_bp, url_prefix='/api/current')

    @app.before_request
    def set_user():
        if str(request.endpoint) != "auth_bp.login" and str(request.endpoint) != "auth_bp.register":
            if request.method != "OPTIONS":
                if "email" in session:
                    from .models import User
                    user = User.query.filter_by(email=session["email"]).first()
                    g.user = user
                    session.permanent = True
                else:
                    return jsonify({"msg": "User not authorized"}), 401

    return app
