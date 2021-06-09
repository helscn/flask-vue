#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint  
from flask_restful import Api

# 从当前路径中导入需要加载的 Restful 资源对象
from .users import UserRes,UsersRes

resources  = Blueprint('api', __name__)
api = Api(resources)

# 将导入的 Restful 资源注册到蓝图中
api.add_resource(UserRes,'/users/<int:id>')
api.add_resource(UsersRes,'/users')
