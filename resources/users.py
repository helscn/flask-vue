#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from auth import login_required, permission_required
from models import User
from flask_restful import abort, Resource


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


class ApiUsers(Resource):
    decorators = [login_required]

    def get(self):
        users = User.query.all()
        return {
            'total': len(users),
            'data': [v.to_dict() for v in users]
        }
