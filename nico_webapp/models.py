from nico_webapp import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
import json


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if not user:
        return None

    if datetime.utcnow() - user.last_login > timedelta(hours=1):
        return None

    return user


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=True, unique=True)
    image_file = db.Column(db.String(120), nullable=False)
    preview_image = db.Column(db.String(120), nullable=True)
    column_span = db.Column(db.Integer, nullable=True)
    row_span = db.Column(db.Integer, nullable=True)
    order_num = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        image = {'image_file': self.image_file, 'title': self.title}
        return json.dumps(image)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(40), nullable=False, unique=True)
    times_visited = db.Column(db.Integer, nullable=False, default=1)
    first_visited = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    last_visited = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    country = db.Column(db.String(20), nullable=True)
    country_flag = db.Column(db.String(80), nullable=True)
