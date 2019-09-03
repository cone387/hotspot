from .parser import Parser, logger, Value, PyQuery
from ..utils.clean import search_time, check_time_in
from urllib.request import urljoin


class CommonParser(Parser):

    name = 'Common'

    def parse_list(self, response):
        selector = self.config['selector']
        if not selector:
            return logger.error("please config %s's selector first", self.config_id)
        doc = PyQuery(response.text)
        data_list = doc(selector)
        yield (Value.HOT_NUM, len(data_list))
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
