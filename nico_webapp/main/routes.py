from flask import Blueprint, render_template, redirect, url_for, current_app, request
from flask_login import login_user, login_required
from flask_mail import Message
from nico_webapp.models import Image, User
from nico_webapp.main.forms import UploadImageForm, EditImageForm, AdminLoginForm, ContactForm
from nico_webapp.main.utils import perform_upload
from nico_webapp import db, mail
import os

main = Blueprint('main', __name__)


@main.route('/')
def home():
    images = Image.query.all()
    return render_template('content.html', images=images)


@main.route('/about/')
def about():
    return render_template('about.html', title='About')


@main.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        msg = Message(subject=subject, sender=email, recipients=['dxtrlbrtry@yahoo.com', 'nico_havia@hotmail.com'])
        msg.body = 'Sender Email: ' + email + '\nSender Name: ' + first_name + ' ' + last_name + '\n\n' + message
        mail.send(msg)
        return redirect(url_for('main.home'))
    return render_template('contact.html', title='Contact', form=form)


@main.route('/admin/', methods=['GET', 'POST'])
def admin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = User.query.filter_by(username=form.username.data).first()
        if admin and admin.password == form.password.data:
            login_user(admin)
            return redirect(url_for('main.manage'))
    return render_template('login.html', form=form)


@main.route('/manage/', methods=['GET'])
@login_required
def manage():
    images = Image.query.all()
    return render_template('manage.html', images=images)


@main.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload_image():
    form = UploadImageForm()
    if form.validate_on_submit():
        image = Image()
        image.title = form.title.data
        image.image_file = perform_upload(form.image.data)
        if form.description.data:
            image.description = form.description.data
        db.session.add(image)
        db.session.commit()
        return redirect(url_for('main.manage'))
    return render_template('upload.html', form=form)


@main.route('/edit/<int:image_id>', methods=['GET', 'POST'])
@login_required
def edit_image(image_id):
    image = Image.query.get_or_404(image_id)
    form = EditImageForm()
    form.title.data = image.title
    form.description.data = image.description
    if form.validate_on_submit():
        image.title = form.title.data
        if form.description.data:
            image.description = form.description.data
        if form.image.data:
            os.remove(os.path.join(current_app.root_path, 'static/pictures/' + image.image_file))
            image.image_file = perform_upload(form.image.data)
        db.session.commit()
        return redirect(url_for('main.manage'))
    return render_template('upload.html', form=form)


@main.route('/delete/<int:image_id>', methods=['GET'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    os.remove(os.path.join(current_app.root_path, 'static/pictures/' + image.image_file))
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for('main.manage'))
