from main import db
from settings import Setting

# 在此处导入需要使用的数据库对象模型
from .roles import Role
from .permissions import Permission
from .users import User


def init_db():
    """删除数据库中所有数据并初始化"""
    db.drop_all()
    db.create_all()

    admin = Role(name='管理员')
    admin.save()

    admin.set_permission('user')
    admin.set_permission('users')

    admin.add_user(username=Setting.DEFAULT_USERNAME,
                   password=Setting.DEFAULT_PASSWORD)

    user = Role(name='普通用户')
    user.save()

    print("The database has been created, the default username is '{}', and the password is '{}'.".format(
        Setting.DEFAULT_USERNAME, Setting.DEFAULT_PASSWORD))
