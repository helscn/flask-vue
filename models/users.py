#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .base_model import db, BaseModel

from itsdangerous import JSONWebSignatureSerializer
from settings import Setting


class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(30))
    department = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(40))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    files = db.relationship(
        'File', backref='user', lazy='dynamic', cascade='all')

    def __init__(self, id, name, title='', department='', phone='', email='', role_id=2):
        self.id = id
        self.name = name
        self.title = title
        self.department = department
        self.phone = phone
        self.email = email
        self.role_id = 2

    def __repr__(self):
        return '<User:{}>'.format(self.name)

    @staticmethod
    def get(user_id):
        """根据用户ID返回用户对象，为 login_user 方法提供支持"""
        if not user_id:
            return None
        return User.query.filter(User.id == user_id).first()

    def generate_token(self):
        """返回当前User对象的验证token"""
        s = JSONWebSignatureSerializer(
            Setting.SECRET_KEY)
        return s.dumps({'id': self.id}).decode('utf-8')

    def generate_response(self):
        response = self.to_dict()
        response['token'] = self.generate_token()
        return response

    @staticmethod
    def verify_token(token):
        """验证 token 是否有效,验证通过时返回User对象"""
        s = JSONWebSignatureSerializer(Setting.SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_dict(self):
        columns = list(
            filter(lambda c: ('password' not in c.name), self.__table__.columns))
        return {c.name: getattr(self, c.name) for c in columns}
