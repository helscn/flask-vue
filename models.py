#!/usr/bin/python3
# -*- coding: utf-8 -*-

from main import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


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


class Config(BaseModel):
    __tablename__ = 'config'
    parameter = db.Column(db.String(128), primary_key=True)
    value = db.Column(db.String(512), unique=True)

    def __repr__(self):
        return '{} = {}'.format(self.parameter, self.value)

    def to_dict(self):
        return {self.parameter: self.value}


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @staticmethod
    def get(user_id):
        """根据用户ID返回用户对象，为 login_user 方法提供支持"""
        if not user_id:
            return None
        return User.query.filter(User.id == user_id)

    def get_id(self):
        return self.id

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self
