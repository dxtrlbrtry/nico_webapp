from flask import Blueprint, render_template, redirect, url_for, current_app, request, jsonify
from flask_login import login_user, login_required
from flask_mail import Message
from nico_webapp.models import Image, User, Visitor
from nico_webapp.main.forms import UploadImageForm, EditImageForm, AdminLoginForm, ContactForm
from nico_webapp.main.utils import perform_upload, register_visitor
from nico_webapp import db, mail
import os
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    register_visitor(request=request)
    images = Image.query.all()
    images.sort(key=lambda x: x.order_num)
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
            admin.last_login = datetime.utcnow()
            db.session.commit()
            login_user(admin)
            return redirect(url_for('main.manage'))
    return render_template('login.html', form=form)


@main.route('/manage/', methods=['GET'])
@login_required
def manage():
    images = Image.query.all()
    images.sort(key=lambda x: x.order_num)
    visitors = len(Visitor.query.all())
    return render_template('manage.html', images=images, visitors=visitors)


@main.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload_image():
    form = UploadImageForm()
    if form.validate_on_submit():
        image = Image()
        image.title = form.title.data
        image.image_file = perform_upload(form.image.data)
        if form.preview_image.data:
            image.preview_image = perform_upload(form.preview_image.data)
        else:
            image.preview_image = image.image_file
        image.order_num = len(Image.query.all()) + 1
        db.session.add(image)
        db.session.commit()
        return redirect(url_for('main.manage'))
    return render_template('upload.html', form=form)


@main.route('/edit/<int:image_id>', methods=['GET', 'POST'])
@login_required
def edit_image(image_id):
    image = Image.query.get_or_404(image_id)
    form = EditImageForm()
    if request.method == 'GET':
        form.title.data = image.title
    if form.validate_on_submit():
        image.title = form.title.data
        if form.preview_image.data:
            if image.preview_image != image.image_file:
                os.remove(os.path.join(current_app.root_path, 'static/pictures/' + image.preview_image))
            image.preview_image = perform_upload(form.preview_image.data)
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
    if image.image_file != image.preview_image:
        os.remove(os.path.join(current_app.root_path, 'static/pictures/' + image.preview_image))
    db.session.delete(image)
    images = Image.query.all()
    images.sort(key=lambda img: img.order_num)
    i = 1
    for img in images:
        img.order_num = i
        i += 1
    db.session.commit()
    return redirect(url_for('main.manage'))


@main.route('/visitors/', methods=['GET'])
@login_required
def visitors():
    visitors = Visitor.query.all()
    return render_template('visitors.html', visitors=visitors)


@main.route('/manage/<int:image_id>/<int:col_span>/<int:row_span>/', methods=['POST'])
@login_required
def apply_span(image_id, col_span, row_span):
    image = Image.query.get_or_404(image_id)
    image.column_span = col_span
    image.row_span = row_span
    db.session.commit()
    return jsonify(success=True)


@main.route('/manage/up/<int:image_id>/', methods=['GET'])
@login_required
def move_up(image_id):
    image = Image.query.get_or_404(image_id)
    if image.order_num > 1:
        above_image = Image.query.filter_by(order_num=image.order_num - 1).first()
        above_image.order_num = image.order_num
        image.order_num -= 1
        db.session.commit()
    return redirect(url_for('main.manage'))


@main.route('/manage/down/<int:image_id>/', methods=['GET'])
@login_required
def move_down(image_id):
    image = Image.query.get_or_404(image_id)
    if image.order_num < len(Image.query.all()):
        below_image = Image.query.filter_by(order_num=image.order_num + 1).first()
        below_image.order_num = image.order_num
        image.order_num += 1
        db.session.commit()
    return redirect(url_for('main.manage'))

