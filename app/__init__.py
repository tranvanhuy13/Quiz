from flask import Flask


def create_app():
    app = Flask(__name__)

    from .routes import quiz_bp
    app.register_blueprint(quiz_bp)

    return app
