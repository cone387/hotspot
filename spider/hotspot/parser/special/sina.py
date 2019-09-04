# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2019-08-26 19:47
# software: PyCharm
import re
import json
from ..parser import Parser, Request, PyQuery
from urllib.request import urljoin


class SinaParser(Parser):
    name = '# 微博热搜'

    def parse_list(self, response):
        # data_str = re.search('\[.*\]', response.text)
        # data_list = json.loads(data_str.group())
        # for data in data_list:
        #     print(data)
        doc = PyQuery(response.text)
        data_list = doc('tbody tr .td-02 a')
        for index, data in enumerate(data_list.items()):
            if not data.attr('href'):
                continue
            item = {
                'url': urljoin(self.config['url'], data.attr('href')),
                'title': data.text(),
                'source': self.config_id,
                'real_pos': index,
                'hot_descr': '',
            }
            yield item

    # def get_start_request(self) -> Request:
    #     request = super().get_start_request()
    #     request['url'] = 'https://s.weibo.com/ajax/jsonp/gettopsug?uid=&ref=PC_topsug&url=https%3A%2F%2Fs.weibo.com%2Ftop%2Fsummary%3FRefer%3Dtop_hot%26topnav%3D1%26wvr%3D6&Mozilla=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_14_1)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36&_cb=STK_15668203175973'
    #     return request