from flask import Flask
from .config import Config
from .extensions import db, migrate, bcrypt, jwt
from .auth.routes import auth_bp
from .tasks.routes import tasks_bp
from flasgger import Swagger

def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Swagger docs
    Swagger(app, template_file=None, config={
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "swagger_ui": True,
        "specs_route": "/docs/"
    })

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    @app.get("/")
    def health():
        return {"status": "ok"}

    return app
