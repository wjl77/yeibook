from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import NumberRange, Length, DataRequired, Regexp


class SearchForm(FlaskForm):
	q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
	page = IntegerField(validators=[NumberRange(min=1)], default=1)


class DriftForm(FlaskForm):
	recipient_name = StringField(validators=[DataRequired('收件人姓名不得为空'), Length(2, 20, '姓名至少2个字符喔')])
	mobile = StringField(validators=[DataRequired('手机号不能为空'),
									 Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
	message = StringField()
	address = StringField(validators=[DataRequired('地址不能为空'),
									  Length(10, 70)])


