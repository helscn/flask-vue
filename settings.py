# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 配置参数


class Setting:
    # 网站静态目录设置,设置为前端build目录
    STATIC_FOLDER = os.path.join(BASE_DIR, 'frontend/dist')

    # 是否允许跨源资源共享访问
    SUPPORT_CORS = True

    # 加密密钥，可以通过 secrets 模块的 secrets.token_hex(16) 获得随机密钥
    # 此密钥用于生成 session ID，cookies 等认证模块
    SECRET_KEY = '06a821a89afd0e1a408a283e5737b3b4'

    # 前端请求谁时，保存 Token 的位置，如 headers, cookies, args, values 等.
    TOKEN_LOCATION = ['headers', 'args']

    # 前端请求认证时，保存 Token 的键值名称
    TOKEN_KEY = 'Token'

    # Token 验证的失效时间
    TOKEN_EXPIRATION = 600

    # 链接数据库
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/test_data.db'.format(BASE_DIR)

    # 跟踪数据库修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 打印输出SqlAlchemy生成的Sql语句
    SQLALCHEMY_ECHO = False

    # 数据库请求结束之后自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 默认初始用户名称
    DEFAULT_USERNAME = 'admin'

    # 默认初始用户密码
    DEFAULT_PASSWORD = '123456'

    # 调试模式
    DEBUG = False
