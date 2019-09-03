# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2019-08-26 19:47
# software: PyCharm
import re
import json
from ..parser import Parser, Request, PyQuery
from urllib.request import urljoin


class SinaParser(Parser):
    name = '知乎热搜'

    def parse_list(self, response):
        data_str = re.search('\{"initialState":.*\}', response.text)
        data_list = json.loads(data_str.group())['initialState']["topstory"]['hotList']
        for index, data in enumerate(data_list):
            item = dict(
                title=data['target']['titleArea']['text'],
                url=data['target']['link']['url'],
                source=self.config_id,
                real_pos=index
            )
            yield item
