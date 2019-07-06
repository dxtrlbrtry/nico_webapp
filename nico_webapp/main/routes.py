from flask import Blueprint, render_template, redirect, url_for
from nico_webapp.models import Image
from nico_webapp.main.forms import ImageForm
from nico_webapp.main.utils import perform_upload
from nico_webapp import db

main = Blueprint('main', __name__)


@main.route('/')
def home():
    images = Image.query.all()
    return render_template('content.html', images=images)


@main.route('/about/')
def about():
    return render_template('about.html', title='About')


@main.route('/contact/')
def contact():
    return render_template('contact.html', title='Contact')


@main.route('/view/<int:image_id>/')
def view(image_id):
    image = Image.query.get_or_404(image_id)
    return render_template('view.html', image=image)


@main.route('/upload/', methods=['GET', 'POST'])
def upload_image():
    form = ImageForm()
    if form.validate_on_submit():
        image = Image()
        image.title = form.title.data
        image.image_file = perform_upload(form.image.data)
        if form.description.data:
            image.description = form.description.data
        db.session.add(image)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('upload.html', form=form)
