import os
from flask import current_app
from PIL import Image


def perform_upload(form_picture):
    picture_path = os.path.join(current_app.root_path, 'static/pictures/', form_picture.filename)

    img = Image.open(form_picture)
    img.thumbnail(img.size)
    img.save(picture_path)

    return form_picture.filename
