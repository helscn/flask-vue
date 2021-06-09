#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from auth import auth
from models import User
from flask_restful import abort, Resource, reqparse

import sys
sys.path.append("..")

userParse = reqparse.RequestParser()
userParse.add_argument('username', type=str)
userParse.add_argument('password', type=str)


class UserRes(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        user = User.get(id)
        if user:
            return {'data': user.to_dict()}
        else:
            abort(404, error='User not exist.')

    def delete(self, id):
        user = User.get(id)
        if user:
            user.delete()
            return '', 204
        else:
            abort(404, error='User not exist.')

    def put(self, id):
        user = User.get(id)
        if user:
            args = userParse.parse_args()
            username = args.get('username')
            password = args.get('password')

            if username:
                new_user = User.query.filter(User.username == username).first()
                if new_user and new_user.id != user.id:
                    abort(406, error='The username already exists.')
                else:
                    user.username = username
            if password:
                if len(password) < 6:
                    abort(406, error='The password is too short.')
                else:
                    user.password = password
            user.save()
            return {'success': True}, 201
        else:
            abort(404, error='User not exist.')


class UsersRes(Resource):
    decorators = [auth.login_required]

    def get(self):
        users = User.query.all()
        return {
            'total': len(users),
            'data': [v.to_dict() for v in users]
        }

    def post(self):
        args = userParse.parse_args()
        username = args.get('username')
        password = args.get('password')
        if not username or not password:
            abort(400, error='Need to provide username or password.')
        user = User.query.filter(User.username == username).first()
        if user:
            abort(406, error='The username already exists.')
        if len(password) < 6:
            abort(406, error='The password is too short.')
        user = User(username, password)
        user.save()
        return {'success': True}, 201


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
