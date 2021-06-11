#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from auth import login_required, permission_required
from models import User
from flask_restful import abort, Resource, reqparse

userParse = reqparse.RequestParser()
userParse.add_argument('username', type=str)
userParse.add_argument('password', type=str)


class ApiUser(Resource):
    decorators = [login_required]

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


class ApiUsers(Resource):

    # 资源名称，用于检查数据库中每个 role 对应的 permission
    # 如果没有定义此资源名，则以当前类名作为资源名
    __resource_name__ = 'users'

    # 默认的资源访问权限，当 role 没有定义对应的资源权限时以此权限为准
    # 如果数据库中和类中均没有定义访问权限，则默认允许访问
    __permission__ = {
        'get': False,
        'post': True
    }

    @login_required
    @permission_required
    def get(self):
        users = User.query.all()
        return {
            'total': len(users),
            'data': [v.to_dict() for v in users]
        }

    @login_required
    @permission_required
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
