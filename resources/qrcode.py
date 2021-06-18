#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from flask import Response
from flask_restful import Resource, reqparse
from io import BytesIO
import qrcode


parser = reqparse.RequestParser()
parser.add_argument('data', type=str, location=['args', 'values'])


class ApiQRCode(Resource):

    def get(self):
        data = parser.parse_args()['data']
        qr = qrcode.make(data=data)
        img = BytesIO()
        qr.save(img, format='JPEG')
        img_bytes = img.getvalue()
        resp = Response(img_bytes, mimetype="image/jpeg")
        return resp
