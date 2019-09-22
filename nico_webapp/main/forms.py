from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from nico_webapp.models import Image
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, length, Email


class UploadImageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(max=20)])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    preview_image = FileField('Preview Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')

    def validate_title(self, title):
        image = Image.query.filter_by(title=title.data).first()
        if image:
            raise ValidationError("File Title Already Exists")


class EditImageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(max=20)])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    preview_image = FileField('Preview Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Authenticate')


class ContactForm(FlaskForm):
    first_name = StringField('First Name *', validators=[DataRequired()])
    last_name = StringField('Last Name *', validators=[DataRequired()])
    email = StringField('Email *', validators=[DataRequired(), Email()])
    subject = StringField('Subject *', validators=[DataRequired()])
    message = TextAreaField('Message *', validators=[DataRequired()])
    submit = SubmitField('Send')
