#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from .base_model import db, BaseModel


class Role(BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rolename = db.Column(db.String(25), nullable=False)
    users = db.relationship('User', backref='role', cascade='all')
    permissions = db.relationship('Permission', backref='role', cascade='all')
