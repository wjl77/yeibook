from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from models.user import User


class RegisterForm(FlaskForm):
	email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='Email错误')])
	password = PasswordField(validators=[DataRequired(message='密码不得为空'), Length(6, 32, message='密码至少需要6位喔')])
	nickname = StringField(validators=[DataRequired(), Length(2, 10, message='必需2-10个字符')])

	def validate_email(self, field):
		# field => 客户端的参数
		email = field.data
		user = User.query.filter_by(email=email).first()
		if user:
			raise ValidationError('电子邮件已被注册')
		return field.data

	def validate_nickname(self, field):
		nickname = field.data
		user = User.query.filter_by(nickname=nickname).first()
		if user:
			raise ValidationError('该昵称已被使用')
		return field.data


class LoginForm(FlaskForm):
	email = StringField(validators=[DataRequired('用户名不得为空喔'), Length(8, 64, '帐号至少需要8个字符喔'),
									Email(message='邮箱帐号格式错误')])
	password = PasswordField(validators=[DataRequired(message='密码不得为空'), Length(6, 32, '密码至少需要6位喔')])


class EmailForm(FlaskForm):
	email = StringField(validators=[DataRequired(), Length(8, 64),
									Email(message='电子邮箱不符合规范')])


class ResetPasswordForm(FlaskForm):
	password1 = PasswordField(validators=[
		DataRequired(),
		Length(6, 32),

	])

	password2 = PasswordField(validators=[
		DataRequired(),
		Length(6, 32),
		EqualTo('password1', message='两次密码不同')
	])




