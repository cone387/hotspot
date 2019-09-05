from cone.spider_ex import CrawlerSpider, logger
from .utils.api import get_config
from .recorder import NewsRecorder
import time
import json
from .parser.manger import ParserManager
from .downloader import NewsDownloader
from .settings import PROCESS_CONFIG_NUM, CONFIG_REGET_DELAY


class HotSpotCrawler(CrawlerSpider):

    block = True
    # recorder = NewsRecorder
    record_queue = 1
    downloader = NewsDownloader
    schedule_delay = 1
    parser_map = {}

    def __init__(self, parser_manager: ParserManager, thread_num):
        self.downloader_num = thread_num
        self.parser_manager = parser_manager
        super().__init__()

    def init_recorder(self):
        pass

    def need_new_parser(self):
        for config_id, parser in list(self.parser_map.items()):
            if not parser.is_working:
                # for board_log in parser.get_crawl_log_list():
                #     collect_logger.info(json.dumps(board_log))
                #     logger.info("[%s][%s]clawl done", configid, board_log['url'])
                log: dict = parser.get_crawl_log()
                logger.info(log)
                NewsRecorder.upadte_item(log)
                del self.parser_map[config_id]
        return len(self.parser_map) < PROCESS_CONFIG_NUM

    def schedule(self):
        if self.need_new_parser():
            config = get_config()
            config_id = config.get('id')
            if config_id in self.parser_map: # 不会爬取重复站点
                return
            parser = self.parser_manager.find_parser(config).instance(config)
            self.parser_map[config_id] = parser
            parser.start_parse()
        else:
            time.sleep(CONFIG_REGET_DELAY)

    def stop(self):
        super().stop()
        NewsRecorder.close()