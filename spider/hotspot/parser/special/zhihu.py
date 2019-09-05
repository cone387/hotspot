# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2019-08-26 19:47
# software: PyCharm
import re
import json
from ..parser import Parser, Value


class SinaParser(Parser):
    name = '知乎热搜'

    def parse_list(self, response):
        data_str = re.search('\{"initialState":.*\}', response.text)
        data_list = json.loads(data_str.group())['initialState']["topstory"]['hotList']
        yield (Value.HOT_NUM, len(data_list))
        for index, data in enumerate(data_list):
            item = dict(
                title=data['target']['titleArea']['text'],
                url=data['target']['link']['url'],
                real_pos=index,
                hot_descr=data['target']['metricsArea']['text']
            )
            yield item
