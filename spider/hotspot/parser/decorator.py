from types import GeneratorType
from cone.spider_ex import Request, logger
from .board_log import BoardLog
from ..abnormal import Abnormal
from ..recorder import NewsRecorder
from cone.tools import get_md5


class Value:
    COLLECT_NUM = 0
    HOT_NUM = 1
    EXIST_BOARD = 2


def collect_parse_log(parse_method):
    def parse_wrapper(parser, response):
        result = parse_method(parser, response)
        if not isinstance(result, GeneratorType):
            return logger.error("empty returned from parse")
        try:
            for item in result:
                if isinstance(item, Request):
                    yield item
                elif isinstance(item, tuple):
                    code, value = item
                    if code == Value.HOT_NUM:
                        parser.log_hot_num += value
                elif isinstance(item, dict):
                    item.update(parser.item)
                    item['hot_md5'] = get_md5(item['url'])
                    if NewsRecorder.record(item):
                        parser.log_upload_num += 1
        except Exception as e:
            logger.info('list error: %s', str(e))
            parser._abnormal = Abnormal.abnormal(code=30, msg=Abnormal.ERROR_SOURCE_DOC[1])
        logger.info("[%s][%s]get %s hot num in %s", parser.config_id, parser.name, parser.log_hot_num, response.url)
        parser._is_working = False
    return parse_wrapper


def collect_log(parser):
    parse_list = getattr(parser, 'parse_list')
    if parse_list.__name__ != 'collect_parse_log':
        parser.parse_list = collect_parse_log(parse_list)
    return parser
