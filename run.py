#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from views import app, db, User, Config

application = app

if len(sys.argv) >= 2:
    # 获取命令行命令
    command = sys.argv[1]

    if command.lower() == 'imgrate':
        db.drop_all()
        db.create_all()
        admin = User(username='admin', password='123456')
        admin.save()
        cfg = Config(parameter='setting', value='OK')
        cfg.save()
        print('''
  The database has been initialized, the default username is 'admin', and the password is '123456'.
''')

    elif command.lower() == 'serve':
        if len(sys.argv) == 3:
            application.run('localhost', int(sys.argv[2]))
        elif len(sys.argv) == 4:
            application.run(sys.argv[2], int(sys.argv[3]))
        else:
            application.run('localhost', 5000)
    else:
        print('''
  Command:
      imgrate : Init the application and install the database.
      serve   : Start the simple web server , the default address is localhost:5000.
        ''')
elif __name__ == '__main__':
    app.run('localhost', 5000)