#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from flask_restful import abort, Resource

import sys 
sys.path.append("..") 
from models import User
from auth import auth

class UserRes(Resource):
    # decorators = [auth.login_required]
    def get(self, id):
        user = User.get(id)
        print('User:',user)
        if user:
            return {'data':user.to_dict()}
        else:
            abort(404,message="User not exist.")

    def delete(self, id):
        user = User.get(id)
        if user:
            user.delete()
        return '', 204

    def put(self, id):
        user = User.get(id)
        if user:
            pass
        return '', 204

class UsersRes(Resource):
    # decorators = [auth.login_required]
    def get(self):
        users=User.query.all()
        return {
            'total':len(users),
            'data':[v.to_dict() for v in users]
        }

    def post(self):
        pass
