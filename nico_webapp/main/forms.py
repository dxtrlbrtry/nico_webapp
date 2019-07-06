from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    submit = SubmitField('Upload')
