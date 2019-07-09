from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'secret'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS']= True
    app.config['MAIL_USERNAME'] = 'flaskzleitner@gmail.com'
    app.config['MAIL_PASSWORD'] = '#Arobs123'
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from nico_webapp.main.routes import main
    app.register_blueprint(main)

    return app
