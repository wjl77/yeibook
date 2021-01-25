from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField


class AvatarForm(FlaskForm):
	avatar = FileField(validators=[FileAllowed(['png', 'jpeg', 'jpg', 'gif'], '只支持png/jpg/jpeg/gif的格式')])
