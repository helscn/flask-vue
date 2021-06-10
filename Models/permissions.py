#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from .base_model import *


class Permission(BaseModel):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, ForeignKey('roles.id'))
    resource = db.Column(db.String(25))
    get = db.Column(db.Boolean, default=False)
    post = db.Column(db.Boolean, default=False)
    put = db.Column(db.Boolean, default=False)
    patch = db.Column(db.Boolean, default=False)
    delete = db.Column(db.Boolean, default=False)
