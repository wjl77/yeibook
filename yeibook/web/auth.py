from flask import render_template, redirect, url_for, request, make_response, flash, jsonify
from flask_login import login_user, logout_user

from forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from libs.email import send_mail
from models.base import db
from models.login_history import LoginHistory
from models.user import User
from .blueprint import web

@web.route('/set/cookie')
def set_cookie():
    response = make_response('测试Cookie')
    response.set_cookie('name', 'lester', 10)
    return response


@web.route('/register', methods=['GET', 'POST'])
def register():
    """ 注册 """
    # from web.right_menus import popular_gifters_list, popular_wishes_list
    form = RegisterForm()
    if form.validate_on_submit():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
            flash('注册成功，请登录', category='success')
        return redirect(url_for('web.login'))
    else:
        if form.errors:
            flash('注册失败，请重试', category='warning')
            print(form.errors)
    return render_template('auth/register.html',
                           form=form)


@web.route('/user/query', methods=['GET', 'POST'])
def user_query():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'is_duplicated': 1})
    return jsonify({'is_duplicated': 0})


@web.route('/nickname/query', methods=['GET', 'POST'])
def nickname_query():
    nickname = request.form.get('nickname')
    nickname = User.query.filter_by(nickname=nickname).first()
    if nickname:
        return jsonify({'is_duplicated': 1})
    return jsonify({'is_duplicated': 0})


@web.route('/login', methods=['GET', 'POST'])
def login():
    """ 登录 """
    # from web.right_menus import popular_gifters_list, popular_wishes_list
    form = LoginForm()
    next = request.values.get('next')

    if form.validate_on_submit():
        keep_cookie = request.form.get('check', None)
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=keep_cookie)
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
            flash('帐号不存在或密码错误', category='warning')
    else:
        if form.errors:
            flash('帐号不存在或密码错误', category='warning')
            print(form.errors)
    return render_template('auth/login.html',
                           form=form,
                           next=next)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    """ 点击忘记密码 """
    # from web.right_menus import popular_gifters_list, popular_wishes_list
    form = EmailForm()
    if form.validate_on_submit():
        account_email = form.email.data
        user = User.query.filter_by(email=account_email).first()
        if user:
            token = user.generate_token()
            try:
                send_mail(account_email, '重置您的密码',
                          'email/reset_password.html',
                          user=user,
                          token=token)
                flash('重置密码的链接已发送到您的邮箱:' + account_email + '，请及时查收', category='success')
                return redirect(url_for('web.login'))
            except:
                flash('发送失败，请检查您的网络')
        else:
            flash('抱歉，您不是本站的用户', category='warning')
    return render_template('auth/forget_password_request.html',
                           form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    # from web.right_menus import popular_gifters_list, popular_wishes_list
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = form.password1.data
        if User.reset_password(token, new_password):
            flash('您的密码已更新，请使用新密码登录', category='success')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败', category='warning')

    return render_template('auth/forget_password.html',
                           form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    """ 注销 """
    logout_user()
    return redirect(url_for('web.index'))
