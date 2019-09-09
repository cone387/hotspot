from .parser import Parser, logger, Value, PyQuery, Abnormal
from ..utils.clean import search_time, check_time_in
from urllib.request import urljoin


class CommonParser(Parser):
    fields_list = ['item_selector', 'link_selector', 'descr_selector']
    name = 'Common'

    def parse_list(self, response):
        item_selector = self.config.get('item_selector')
        doc = PyQuery(response.text)
        data_list = doc(item_selector)
        yield (Value.HOT_NUM, len(data_list))
        for index, data in enumerate(data_list.items()):
            link = data(self.config['link_selector'])
            if not link.attr('href'):
                continue
            if self.link_trash_selector:
                link(self.link_trash_selector).remove()
            hot_descr = data(self.config['descr_selector'])
            if self.descr_trash_selector:
                hot_descr(self.descr_trash_selector).remove()
            item = {
                'url': urljoin(self.config['url'], link.attr('href')),
                'title': link.text(),
                'hot_descr': hot_descr.text(),
                'real_pos': index,

            }
            yield item

    def check_fields(self):
        for field in self.fields_list:
            if not self.config.get(field):
                self._abnormal = Abnormal.abnormal(f"{field} not found")
                return False
        return True

