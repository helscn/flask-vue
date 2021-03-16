#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from views import app, db, User, Config

application = app
application.run('0.0.0.0', 8080)

if len(sys.argv) >= 2:
    # 获取命令行命令
    command = sys.argv[1]

    if command == 'imgrate':
        db.drop_all()
        db.create_all()
        admin = User(username='admin', password='123456')
        admin.save()
        cfg = Config(parameter='setting', value='OK')
        cfg.save()
        print('''
  The database has been initialized, the default username is 'admin', and the password is '123456'.
''')

    elif command == 'server':
        application.run('0.0.0.0', 8080)

    else:
        print('Unknow command!')

elif __name__ == '__main__':
    print('''
  Command:
      imgrate : Init the application and install the database
      server  : Start the simple web server to localhost:5000
    ''')
