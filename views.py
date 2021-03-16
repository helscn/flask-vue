#!/usr/bin/python3
# -*- coding: utf-8 -*-

from forms import LoginForm
import requests
import mimetypes
from main import app
from models import db, Config, User

from flask import Flask, Response, flash, request, session, redirect, url_for, send_file, abort
from flask import jsonify, render_template, make_response

from flask_login import LoginManager
# login_required 要放在 route 装饰器后面
from flask_login import current_user, login_user, logout_user, login_required
from flask_restful import Api
from flask_restful import Resource
api = Api(app)


# 导入表单

# 登陆管理设置
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
    # return render_template('index.html')
    return app.send_static_file('index.html')


@app.route('/password/<password>')
@login_required
def change_password(password):
    try:
        current_user.set_password(password).save()
        return jsonify({
            "success": True,
            "message": 'ok'
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": err.args[0]
        })


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 账号数据库验证账号登陆
    if current_user.is_authenticated:
        return redirect('/')
    emsg = ""
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form, emsg=emsg)
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        if user and user.verify_password(password):
            login_user(user)
            # return redirect(request.args.get('next') or url_for('index'))
            return redirect('/')
        else:
            emsg = "用户名或密码错误！"
            return render_template('login.html', form=form, emsg=emsg)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('已经登出.')
    return redirect('/login')


@app.route('/config')
@login_required
def query_all_config():
    return jsonify([{v.parameter: v.value for v in Config.query.all()}])


@app.route('/config/<parameter>')
def query_config(parameter):
    para = Config.query.filter(Config.parameter == parameter).first()
    if para:
        return jsonify(para.value)
    else:
        return jsonify('')


@app.route('/add/<username>')
def add_user(username):
    usr = User(username=username, password='123')
    # usr.save()
    db.session.add(usr)
    db.session.commit()
    return jsonify('ok')


# 文件代理下载示例
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        url = "http://docs.jinkan.org/docs/flask/quickstart.html"
        r = requests.get(url, timeout=500)
        if r.status_code != 200:
            raise Exception(
                "Cannot connect with oss server or file is not existed.")
        response = make_response(r.content)
        mime_type = mimetypes.guess_type(filename)[0]
        response.headers['Content-Type'] = mime_type
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
            filename.encode().decode('latin-1'))
        return response
    except Exception as err:
        print('download_file error: {}'.format(str(err)))


# Restful API示例
class Hello(Resource):
    @staticmethod
    def get():
        return "[get] hello flask"

    @staticmethod
    def post():
        return "[post] hello flask"


api.add_resource(Hello, '/hello')


# 错误页面请求处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
