# -*- coding: utf-8 -*-

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# 配置参数
class Setting:
    # 加密密钥
    SECRET_KEY = 'my_secret@helscn'

    # 链接数据库
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/data.db'.format(BASE_DIR)

    # 跟踪数据库修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    
    # 打印输出SqlAlchemy生成的Sql语句
    SQLALCHEMY_ECHO = True

    # 数据库请求结束之后自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 调试模式
    DEBUG = False

