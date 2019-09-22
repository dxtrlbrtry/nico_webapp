import os
import secrets
import requests
from nico_webapp.models import Visitor
from nico_webapp import db
from datetime import datetime, timedelta
from flask import current_app
from PIL import Image


def perform_upload(form_picture):
    random_hex = secrets.token_hex(4)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + '_' + random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pictures/', picture_fn)

    img = Image.open(form_picture)
    img.thumbnail(img.size)
    img.save(picture_path, quality=2540)

    return picture_fn


def register_visitor(request):
    url = 'https://api.ipgeolocation.io/ipgeo?apiKey=201be47153114765862e8410daf26659&ip='
    addr = (str)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        addr = request.environ['REMOTE_ADDR']
    else:
        addr = request.environ['HTTP_X_FORWARDED_FOR']
    visitor = Visitor.query.filter_by(ip_address=addr).first()
    if visitor:
        if datetime.utcnow() - visitor.last_visited > timedelta(minutes=30):
            visitor.times_visited = visitor.times_visited + 1
        visitor.last_visited = datetime.utcnow()
        if visitor.country is None:
            geoloc = requests.get(url + addr)
            if geoloc.status_code == 200:
                visitor.country = geoloc.json()['city'] + ', ' + geoloc.json()['country_name']
                visitor.country_flag = geoloc.json()['country_flag']
    else:
        new_visitor = Visitor(ip_address=addr)
        geoloc = requests.get(url + addr)
        if geoloc.status_code == 200:
            new_visitor.country = geoloc.json()['city'] + ', ' + geoloc.json()['country_name']
            new_visitor.country_flag = geoloc.json()['country_flag']
        db.session.add(new_visitor)
    db.session.commit()
