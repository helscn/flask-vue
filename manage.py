#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from views import app
from models import db, init_db

application = app

if len(sys.argv) >= 2:
    # 获取命令行命令
    command = sys.argv[1].lower()

    if command == 'dropdb':
        q = input('Are you sure you want to delete all database data?[Y/N]')
        if q.upper() == 'Y':
            db.drop_all()
            print('All data has been deleted.')

    elif command == 'initdb':
        init_db()

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
      initdb : Init the application and install the database.
      dropdb  : Delete all database data.
      serve   : Start the simple web server , the default address is localhost:5000.
        ''')
elif __name__ == '__main__':
    app.run('localhost', 5000)
