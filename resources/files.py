#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from auth import login_required, permission_required
from models import File
from settings import Setting
from flask import g, request
from flask_restful import abort, Resource
from os import path, remove


class ApiFile(Resource):
    # @login_required
    def get(self, id):
        file = File.get(id)
        if file:
            return file.response()
        else:
            abort(404, error='File not exist.')

    @login_required
    def delete(self, id):
        file = File.get(id)
        if file:
            if file.user_id != g.current_user.id:
                abort(401, error='Unauthorized access')
            try:
                remove(path.join(Setting.UPLOAD_FOLDER, file.save_name))
            except:
                abort(404, error='File not exist.')
            file.delete()
            return '', 204
        else:
            abort(404, error='File not exist.')


class ApiFiles(Resource):
    @login_required
    def get(self):
        user = g.current_user
        files = File.query.filter_by(user_id=user.id).all()
        return {
            'total': len(files),
            'data': [v.to_dict() for v in files]
        }

    @login_required
    @permission_required
    def post(self):
        for name in request.files:
            file = request.files.get(name)
            filename = path.basename(file.filename)
            ext = path.splitext(filename)[1]
            mimetype = file.mimetype
            user_id = g.current_user.id
            attachment = File(
                name=filename, ext=ext, mimetype=mimetype, user_id=user_id)
            attachment.save()
            file.save(path.join(Setting.UPLOAD_FOLDER, attachment.save_name))
        return {'success': True}, 201
