from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, SelectField


class ResourceUploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])


class ResourceKeyModifyForm(FlaskForm):
    submit = SubmitField("Modify")

