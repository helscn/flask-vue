#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Setting

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# 初始化app,取消显示静态资源的 statice 路由
app = Flask(__name__, static_url_path='', static_folder=Setting.STATIC_FOLDER)

# 载入配置
app.config.from_object(Setting)

# 全局跨域访问设置
if Setting.SUPPORT_CORS:
    from flask_cors import CORS
    CORS(app, supports_credentials=True)

# 数据库模型对象
db = SQLAlchemy(app)
