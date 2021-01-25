from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api.views import api
from libs.filters import timeago_format, month_format
from models.base import db
from models.user import User
from web.blueprint import web


app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('secure')
#
mail = Mail()
mail.init_app(app=app)
#
login_manager = LoginManager()
login_manager.init_app(app=app)
login_manager.login_view = 'web.login'
# login_manager.login_message = '请先登录或注册'
#
app.register_blueprint(web)
app.register_blueprint(api)
#
manager = Manager(app)
#
db.init_app(app=app)
#
migrate = Migrate(app=app, db=db)
#
manager.add_command('db', MigrateCommand)
db.create_all(app=app)
#
app.jinja_env.filters['timeago_format'] = timeago_format
app.jinja_env.filters['month_format'] = month_format


@login_manager.user_loader
def get_user(uid):
	return User.query.get(int(uid))


@app.errorhandler(404)
def not_found(e):
	# print(e)
	return render_template('404.html'), 404


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=81, debug=app.config['DEBUG'], threaded=True)
	# manager.run()
