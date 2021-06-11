from main import db
from settings import Setting

# 在此处导入需要使用的数据库对象模型
from .permissions import Permission
from .roles import Role
from .users import User


def init_db():
    """删除数据库中所有数据并初始化"""
    db.drop_all()
    db.create_all()

    role = Role(rolename='管理员')

    users_permission = Permission(
        role_id=role.id,
        resource='users',
        get=True,
        post=True,
        put=False,
        patch=False,
        delete=False
    )

    user_permission = Permission(
        role_id=role.id,
        resource='users',
        get=True,
        post=True,
        put=True,
        patch=True,
        delete=True
    )

    user = User(username=Setting.DEFAULT_USERNAME,
                password=Setting.DEFAULT_PASSWORD,
                role_id=role.id
                )
    role.users.add(user)
    role.permissions.add(users_permission)
    role.permissions.add(user_permission)

    try:
        role.save()
        print("The database has been created, the default username is '{}', and the password is '{}'.".format(
            Setting.DEFAULT_USERNAME, Setting.DEFAULT_PASSWORD))
    except:
        print('Failed to initialize the database')