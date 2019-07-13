from nico_webapp import db, login_manager
from flask_login import UserMixin
import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(60), nullable=True, unique=True)
    description = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        image = {'image_file': self.image_file, 'title': self.title, 'description': self.description }
        return json.dumps(image)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
