#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from flask import g, Blueprint
from flask_restful import Api, abort, Resource, reqparse
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from Models import User
from settings import Setting


##################### 资源权限验证 #############################

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


##################### 资源请求验证 #############################
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='')
multi_auth = MultiAuth(token_auth, basic_auth)

auth = token_auth

tokenParse = reqparse.RequestParser()
tokenParse.add_argument(Setting.TOKEN_KEY, dest='token',
                        type=str, location=Setting.TOKEN_LOCATION, required=False)


@token_auth.verify_token
def verify_token(token):
    g.current_user = None
    args = tokenParse.parse_args()
    token = args.get('token')
    if not token:
        return False
    else:
        g.current_user = User.verify_token(token)
        return g.current_user is not None


@basic_auth.verify_password
def verify_password(username, password):
    g.current_user = None
    user = User.query.filter(User.username == username).first()
    if user and user.verify_password(password):
        g.current_user = user
        return True
    else:
        return False


@token_auth.error_handler
def auth_error():
    return abort(401, message='Unauthorized access')


@basic_auth.error_handler
def auth_error():
    return abort(401, message='Unauthorized access')


##################### 账号登录验证 #############################

# 客户端登录认证
class Login(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str, required=True,
                           help='Username is required.')
        parse.add_argument('password', type=str, required=True,
                           help='Password is required.')
        args = parse.parse_args()
        user = User.query.filter(User.username == args['username']).first()
        if user and user.verify_password(args['password']):
            return {
                'userid': user.id,
                'username': user.username,
                'token': user.generate_token(Setting.TOKEN_EXPIRATION),
                'expiration': Setting.TOKEN_EXPIRATION
            }
        else:
            abort(401, message='Username or passowrd is incorrect!')

# 客户端请求获取新token


class GetToken(Resource):
    decorators = [auth.login_required]

    def get(self):
        args = tokenParse.parse_args()
        token = args.get('token')
        user = User.verify_token(token)
        if user:
            g.current_user = user
            return {
                'userid': user.id,
                'username': user.username,
                'token': user.generate_token(Setting.TOKEN_EXPIRATION),
                'expiration': Setting.TOKEN_EXPIRATION
            }
        else:
            abort(401, message='Unauthorized access')


# 注册登录路由至 login 蓝图中
login = Blueprint('login', __name__)
api = Api(login)
api.add_resource(Login, '/login')
api.add_resource(GetToken, '/gettoken')