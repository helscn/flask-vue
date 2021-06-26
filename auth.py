#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from functools import wraps
from requests import Session
from flask import g, Blueprint
from flask_restful import Api, abort, Resource, reqparse
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from models import User
from settings import Setting


##################### 资源权限验证 #############################

def permission_required(func):
    # 用户访问资源接口的权限检查函数，此装饰器必须放在登录auth验证装饰器后面
    # 且只能用于单独装饰函数，不能放在资源 decorators 中
    @wraps(func)
    def wrap_func(cls, *args, **kwargs):

        # 请求的资源名称，用于验证对应资源的权限
        # 如果资源类存在 __resource_name__ 属性则以 __resource_name__ 作为资源名称
        # 否则以资源定义的类名作为资源名称
        resource_name = getattr(
            cls.__class__, '__resource_name__', cls.__class__.__name__)

        # 如果数据库中未设置此资源的权限，则以资源类的 __permission__ 判断权限
        # 如果 __permission__ 也不存在，则默认允许访问
        default_permission = cls.__permission__ if hasattr(
            cls, '__permission__') else None

        # 请求方法名称，如get,put,delete等
        method = func.__name__.lower()

        # 获取当前登录的用户
        current_user = g.current_user
        if not current_user:
            abort(401, error='Unauthorized access')

        # 检查当前用户对资源的访问权限，优先判断数据库中设置的权限
        # permission = current_user.role.get_resource_permission(resource_name)
        permission = current_user.role.permissions.filter_by(
            resource=resource_name).first()
        if permission is None:
            permission = default_permission
        else:
            permission = permission.to_dict()

        if permission and permission.get(method, True) == False:
            abort(403, error='Access forbidden')

        # 如果该用户有资源访问权限，则正常调用函数
        return func(cls, *args, **kwargs)

    return wrap_func


##################### 请求账号验证 #############################
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='')
multi_auth = MultiAuth(token_auth, basic_auth)

# 默认以 Token 验证，也可以使用 Basic Http 验证或多重验证
login_required = token_auth.login_required

tokenParse = reqparse.RequestParser()
tokenParse.add_argument(Setting.TOKEN_KEY, dest='token',
                        type=str, location=Setting.TOKEN_LOCATION, required=False)


# Token 验证函数
@ token_auth.verify_token
def verify_token(token):
    g.current_user = None
    args = tokenParse.parse_args()
    token = args.get('token')
    if not token:
        return False
    else:
        g.current_user = User.verify_token(token)
        return g.current_user is not None


# Basic Http 验证函数
@ basic_auth.verify_password
def verify_password(username, password):
    g.current_user = None
    user = User.query.filter(User.username == username).first()
    if user and user.verify_password(password):
        g.current_user = user
        return True
    else:
        return False


# Token 验证错误处理函数
@ token_auth.error_handler
def auth_error():
    abort(401, error='Unauthorized access')


# Basic Http 验证错误处理函数
@ basic_auth.error_handler
def auth_error():
    abort(401, error='Unauthorized access')


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
        userid = args['username'].strip()
        password = args['password']
        LOGIN_URL = 'http://eip.sye.com.cn/bpm/login'
        QUERY_URL = 'http://eip.sye.com.cn/bpm/r?wf_num=R_S007_B016&wf_gridnum=V_S007_G012'

        session = Session()
        res = session.post(url=LOGIN_URL, data={
            'UserName': userid,
            'Password': password
        })
        if '用户名或密码错误' in res.text:
            abort(401, error='Username or passowrd is incorrect!')
        res = session.post(url=QUERY_URL, data={
            'm': userid
        })
        users = res.json()['rows']
        userinfo = None
        for u in users:
            if u['Userid'] == userid:
                userinfo = {
                    'id': u['Userid'],
                    'name': u['CnName'],
                    'title': u['JobTitle'],
                    'department': u['FolderName'],
                    'phone': u['PhoneNumber'],
                    'email': u['InternetAddress'],

                }
                break

        user = User.query.filter_by(id=userid).first()

        if user:
            user.name = userinfo['name']
            user.title = userinfo['title']
            user.department = userinfo['department']
            user.phone = userinfo['phone']
            user.email = userinfo['email']
        else:
            user = User(**userinfo)
        user.save()
        return user.generate_response()


# 客户端请求获取新token
class GetToken(Resource):
    @ login_required
    def get(self):
        args = tokenParse.parse_args()
        token = args.get('token')
        user = User.verify_token(token)
        if user:
            g.current_user = user
            return user.generate_response()
        else:
            abort(401, error='Unauthorized access')


# 注册登录路由至 login 蓝图中
UserLogin = Blueprint('auth', __name__)
api = Api(UserLogin)
api.add_resource(Login, '/login')
api.add_resource(GetToken, '/gettoken')
