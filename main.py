#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# 初始化app,取消显示静态资源的 statice 路由
app = Flask(__name__, static_url_path='', static_folder='frontend/dist')

# 全局跨域访问设置
CORS(app, supports_credentials=True)

# 载入配置
app.config.from_object('settings.Setting')

db = SQLAlchemy(app)
