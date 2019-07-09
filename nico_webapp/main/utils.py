import os
import secrets, jwt
from flask import current_app, session, abort
from PIL import Image
from functools import wraps
from flask_jwt_extended import decode_token
from nico_webapp.models import User


def perform_upload(form_picture):
    random_hex = secrets.token_hex(4)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + '_' + random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pictures/', picture_fn)

    img = Image.open(form_picture)
    img.thumbnail(img.size)
    img.save(picture_path)

    return picture_fn


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = jwt.decode(session['access_token'])
        if not User.query.filter_by(username=token['identity']):
            return abort(404)
        return f(*args, **kwargs)
    return decorated()
