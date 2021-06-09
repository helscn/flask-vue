#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer
from settings import Setting

# 初始化app,取消显示静态资源的 statice 路由
app = Flask(__name__, static_url_path='', static_folder=Setting.STATIC_FOLDER)

# 载入配置
app.config.from_object('settings.Setting')

# 全局跨域访问设置
if Setting.SUPPORT_CORS:
    from flask_cors import CORS
    CORS(app, supports_credentials=True)

# 数据库模型对象
db = SQLAlchemy(app)


class BaseModel(db.Model):
    __abstract__ = True   # 声明当前类为抽象类，被继承调用不被创建

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25))
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @staticmethod
    def get(user_id):
        """根据用户ID返回用户对象，为 login_user 方法提供支持"""
        if not user_id:
            return None
        return User.query.filter(User.id == user_id).first()

    def get_id(self):
        return self.id

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expiration):
        """返回当前User对象的验证token"""
        s = TimedJSONWebSignatureSerializer(
            Setting.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        """验证 token 是否有效,验证通过时返回User对象"""
        s = TimedJSONWebSignatureSerializer(Setting.SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_dict(self):
        columns = list(
            filter(lambda c: ('password' not in c.name), self.__table__.columns))
        return {c.name: getattr(self, c.name) for c in columns}


def create_database():
    """删除数据库中所有数据并初始化"""
    db.create_all()
    admin = User(username=Setting.DEFAULT_USERNAME,
                 password=Setting.DEFAULT_PASSWORD)
    try:
        admin.save()
        print("The database has been created, the default username is '{}', and the password is '{}'.".format(
            Setting.DEFAULT_USERNAME, Setting.DEFAULT_PASSWORD))
    except:
        print("The default 'admin' user already exists.")


def permission_required(func):
    from flask import g
    from functools import wraps

    @wraps(func)
    def wrap_func(cls, *args, **kwargs):
        method = func.__name__
        resource = cls.__class__.__name__
        current_user = g.current_user

        if hasattr(cls, '__resource__'):
            resource = cls.__resource__
        # 如果不存在权限，则返回
        return func(cls, *args, **kwargs)

    return wrap_func


class Permission(BaseModel):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer)
    resource = db.Column(db.String(25))
    get = db.Column(db.Boolean)
    post = db.Column(db.Boolean)
    put = db.Column(db.Boolean)
    patch = db.Column(db.Boolean)
    delete = db.Column(db.Boolean)


class Role(BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25))
