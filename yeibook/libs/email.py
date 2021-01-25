from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from fisher import mail


def send_async_email(app, msg):
	with app.app_context():
		try:
			mail.send(msg)
		except Exception as e:
			pass


def send_mail(to, subject, template, **kwargs):
	# msg = Message('叶书测试邮件', sender='550310889@qq.com',
	# 			  body='叶书测试', recipients=['550310889@qq.com'])
	msg = Message('叶书 ' + subject,
				  sender=current_app.config['MAIL_USERNAME'],
				  recipients=[to])
	msg.html = render_template(template, **kwargs)
	# mail.send(msg)
	app = current_app._get_current_object()
	th1 = Thread(target=send_async_email, args=[app, msg])
	th1.start()

