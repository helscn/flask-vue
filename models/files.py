#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from flask import send_from_directory
from settings import Setting
from urllib.parse import quote
from .base_model import db, BaseModel


class File(BaseModel):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    ext = db.Column(db.String(256), nullable=False)
    mimetype = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def get(file_id):
        """根据文件ID返回文件对象"""
        if not file_id:
            return None
        return File.query.filter_by(id=file_id).first()

    @property
    def save_name(self):
        return '{id}{ext}'.format(id=self.id, ext=self.ext)

    def response(self):
        response = send_from_directory(
            Setting.UPLOAD_FOLDER, self.save_name)
        response.headers["Content-Disposition"] = \
            "attachment;" \
            "filename*=UTF-8''{utf_filename}".format(
                utf_filename=quote(self.name.encode('utf-8'))
        )
        return response
