#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from .base_model import *


class Role(BaseModel):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rolename = db.Column(db.String(25), nullable=False)
    # users = relationship('User', backref='roles')
    permissions = relationship('Permission', backref='roles')
