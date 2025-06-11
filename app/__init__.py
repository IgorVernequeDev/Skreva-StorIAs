from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'skrevastorias'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skreva.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes.main import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
