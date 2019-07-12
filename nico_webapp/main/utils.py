import os
import secrets
from flask import current_app
from PIL import Image


def perform_upload(form_picture):
    random_hex = secrets.token_hex(4)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + '_' + random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pictures/', picture_fn)

    img = Image.open(form_picture)
    img.thumbnail(img.size)
    img.save(picture_path)

    return picture_fn
