from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, length


class UploadImageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(max=20)])
    description = TextAreaField('Description', validators=[])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    preview = FileField('Upload Preview', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')


class EditImageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(max=20)])
    description = TextAreaField('Description', validators=[])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    preview = FileField('Upload Preview', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Authenticate')


class ContactForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Authenticate')
