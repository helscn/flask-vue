#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main import app
from auth import login
from Resources import resources

# 注册登录 login 蓝图
app.register_blueprint(login, url_prefix='/')

# 注册 Restful API 蓝图
app.register_blueprint(resources, url_prefix='/api')


# 注册前端主页路由
@app.route('/')
@app.route('/index')
def index():
    return app.send_static_file('index.html')

# # 默认的错误页面请求处理
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500
