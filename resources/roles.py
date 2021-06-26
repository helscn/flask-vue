#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from auth import login_required, permission_required
from models import Role
from flask_restful import abort, Resource, reqparse


class ApiRole(Resource):
    # 资源名称，用于检查数据库中每个 role 对应的 permission
    # 如果没有定义此资源名，则以当前类名作为资源名
    __resource_name__ = 'roles'

    # 默认的资源访问权限，当 role 没有定义对应的资源权限时以此权限为准
    # 如果数据库中和类中均没有定义访问权限，则默认允许访问
    __permission__ = {
        'get': True,
        'delete': False
    }

    @login_required
    @permission_required
    def get(self, id):
        role = Role.get(id)
        if role:
            return {'data': role.to_dict()}
        else:
            abort(404, error='Role not exist.')

    @login_required
    @permission_required
    def delete(self, id):
        role = Role.get(id)
        if role:
            role.delete()
            return '', 204
        else:
            abort(404, error='Role not exist.')


class ApiRoles(Resource):
    # 资源名称，用于检查数据库中每个 role 对应的 permission
    # 如果没有定义此资源名，则以当前类名作为资源名
    __resource_name__ = 'roles'

    # 默认的资源访问权限，当 role 没有定义对应的资源权限时以此权限为准
    # 如果数据库中和类中均没有定义访问权限，则默认允许访问
    __permission__ = {
        'get': True,
        'post': False
    }

    @login_required
    @permission_required
    def get(self):
        roles = Role.query.all()
        return {
            'total': len(roles),
            'data': [v.to_dict() for v in roles]
        }

    @login_required
    @permission_required
    def post(self):
        roleParse = reqparse.RequestParser()
        roleParse.add_argument('name', type=str)
        args = roleParse.parse_args()
        role_name = args.get('name')
        if not role_name:
            abort(400, error='Need to provide rolename.')
        role = Role.query.filter_by(name=role_name).first()
        if role:
            abort(406, error='The rolename already exists.')
        role = Role(name=role_name)
        role.save()
        return {'success': True}, 201
