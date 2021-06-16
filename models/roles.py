#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from .base_model import db, BaseModel
from .permissions import Permission
from .users import User


class Role(BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)
    users = db.relationship(
        'User', backref='role', lazy='dynamic', cascade='all')
    permissions = db.relationship(
        'Permission', backref='role', lazy='dynamic', cascade='all')

    @staticmethod
    def get(role_id):
        """根据角色ID返回角色对象"""
        if not role_id:
            return None
        return Role.query.filter(Role.id == role_id).first()

    def add_permission(self, resource, **kwargs):
        # 新建资源访问权限
        permission = Permission(role_id=self.id, resource=resource, **kwargs)
        permission.save()

    def set_permission(self, resource, **kwargs):
        # 修改角色访问的资源权限，当未设置过对应权限时会新建该资源的访问权限
        permission = Permission.query.filter_by(
            role_id=self.id, resource=resource).first()
        if not permission:
            self.add_permission(resource, **kwargs)
        else:
            for kw in kwargs:
                if kw in ('get', 'post', 'put', 'patch', 'delete'):
                    setattr(permission, kw, kwargs[kw])
            permission.save()

    def add_user(self, username, password):
        user = User(username=username, password=password, role_id=self.id)
        user.save()
