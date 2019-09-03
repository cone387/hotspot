# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2019-08-26 09:39
# software: PyCharm
from django.http import HttpResponse
from datetime import datetime
import json


class ConfigEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(o)


class ApiResponse(HttpResponse):
    def __init__(self, data=None, success=True, code=0):
        response = {
            'success': success,
            'data': data,
            'code': code
        }
        super().__init__(json.dumps(response, ensure_ascii=False, cls=ConfigEncoder), content_type='application/json')
        self["Access-Control-Allow-Origin"] = "*"
        self["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        self["Access-Control-Max-Age"] = "1000"
        self["Access-Control-Allow-Headers"] = "*"

    def __len__(self):
        return 1