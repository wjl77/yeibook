from flask import render_template, redirect, url_for, request, make_response, flash
from flask_login import login_user, logout_user

from forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from libs.email import send_mail
from models.base import db
from models.login_history import LoginHistory
from models.user import User
from .blueprint import web

__author__ = '七月'


@web.route('/set/cookie')
def set_cookie():
    response = make_response('测试Cookie')
    response.set_cookie('name', 'lester', 10)
    return response


@web.route('/register', methods=['GET', 'POST'])
def register():
    """ 注册 """
    form = RegisterForm()
    if form.validate_on_submit():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    """ 登录 """
    form = LoginForm()
    next = request.values.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            with db.auto_commit():
                login_history = LoginHistory()
                login_history.uip = request.remote_addr
                login_history.uag = request.headers.get('user-agent')
                login_history.uid = user.id
                db.session.add(login_history)
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('帐号不存在或密码错误', category='alert')
    else:
        if form.errors:
            print(form.errors)
    return render_template('auth/login.html', form=form, next=next)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    """ 点击忘记密码 """
    form = EmailForm()
    if form.validate_on_submit():
        account_email = form.email.data
        user = User.query.filter_by(email=account_email).first()
        if user:
            token = user.generate_token()
            try:
                send_mail(account_email, '重置你的密码',
                          'email/reset_password.html',
                          user=user,
                          token=token)
                flash('重置密码已发送到你的邮箱' + account_email + '，请及时查收')
                return redirect(url_for('web.login'))
            except:
                flash('发送失败，请检查您的网络')
        else:
            flash('抱歉，你不是本站的用户')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = form.password1.data
        if User.reset_password(token, new_password):
            flash('你的密码已更新，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')

    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    """ 注销 """
    logout_user()
    return redirect(url_for('web.index'))
