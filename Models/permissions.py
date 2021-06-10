#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from .base_model import db, BaseModel


class Permission(BaseModel):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # 权限配置的资源名称，使用小写命名
    # 默认为资源对象类的小写，如果有 __resource__ 则使用 __resource__ 对应的资源名
    resource = db.Column(db.String(25))

    # 接口访问类型权限设置，True为允许访问
    get = db.Column(db.Boolean, default=False)
    post = db.Column(db.Boolean, default=False)
    put = db.Column(db.Boolean, default=False)
    patch = db.Column(db.Boolean, default=False)
    delete = db.Column(db.Boolean, default=False)
