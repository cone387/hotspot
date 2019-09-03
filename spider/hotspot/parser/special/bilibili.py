# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2019-08-26 19:47
# software: PyCharm
import re
import json
from ..parser import Parser, Request, PyQuery
from urllib.request import urljoin


class BiliBili(Parser):
    name = '#全站热榜'

    def parse_list(self, response):
        doc = PyQuery(response.text)
        data_list = doc('.rank-item .info a')
        for index, data in enumerate(data_list.items()):
            if not data.attr('href'):
                continue
            item = {
                'url': urljoin(self.config['url'], data.attr('href')),
                'title': data.text(),
                'source': self.config_id,
                'real_pos': index
            }
            yield item
