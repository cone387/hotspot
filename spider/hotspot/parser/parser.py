from cone.spider_ex import logger, Request
from ..abnormal import Abnormal
import time
from ..log import HotspotLog
from .decorator import collect_log, Value
from cone.pyquery_ex import PyQuery


class Parser:
    name = None
    id = None

    def __init__(self, config: dict):
        self.config = config
        self.config_id = config.get('id')
        self._abnormal = Abnormal.NONE
        self.log = HotspotLog(source_id=self.config_id)

        self._is_working = False

        # 基础request参数
        self._encoding = config.get('charset', 'utf-8') or 'utf-8'
        # 每一条要保存信心所必须有的信息
        self.item = {
            'is_test': self.config.get('is_test', '0') == '1',
            'source': self.config_id,
        }

        self.link_trash_selector = self.config.get('link_trash_selector')
        self.descr_trash_selector = self.config.get('descr_trash_selector')

        self.log_url_error = 0
        self.log_doc_error = 0
        self.log_hot_num = 0
        self.log_upload_num = 0
        self.log_except_num = self.config.get('default_count')
        self.log_start_time = time.strftime('%Y-%m-%d %H:%M:%S')

    def get_crawl_log(self):
        if self._abnormal != Abnormal.NONE:
            abnormal, warn_msg = self._abnormal
        elif self.log_url_error:
            abnormal, warn_msg = Abnormal.ERROR_SOURCE_URL
        elif self.log_doc_error:
            abnormal, warn_msg = Abnormal.ERROR_SOURCE_DOC
        elif self.log_hot_num == 0:
            abnormal, warn_msg = Abnormal.EMPTY_HOT_NUM
        elif self.log_except_num > self.log_hot_num:
            abnormal, warn_msg = Abnormal.WARN_HOT_NUM
        else:
            abnormal, warn_msg = Abnormal.NONE
        warn_msg = f'[{self.log_upload_num}|{self.log_hot_num}|{self.log_except_num}]{warn_msg}'
        logger.info("[%s][%s][%s]clawl done, get %s/%s hotspot", self.config_id, self.config['name'], self.name, self.log_upload_num, self.log_hot_num)
        return dict(
            source_id=self.config_id,
            abnormal=abnormal,
            warn_msg=warn_msg,
            last_runtime=self.log_start_time
        )

    def parse_list(self, response):  # 通用获取解析帖子列表
        raise NotImplementedError

    def list_error(self, response): # 处理列表页错误的url, 该板块有问题
        self.log.source_url_error = True
        self._is_working = False

    def get_start_request(self) -> Request:
        return Request(
            url=self.config['url'],
            encoding=self.config.get('charset', 'utf-8') or 'utf-8',
            callback=self.parse_list,
            do_filter=False,
            errorcall=self.list_error
        )

    @property
    def is_working(self):
        return self._is_working

    def check_fields(self):
        return True

    def start_parse(self):
        if self.check_fields():
            request = self.get_start_request()
            if isinstance(request, Request):
                self._is_working = True
                request.start_request()
            else:
                logger.warn('start request not found')
                self.set_abnormal(Abnormal.ERROR_START_REQUEST)

    @classmethod
    def instance(cls, config):
        cls = collect_log(cls)
        return cls(config)

# 标题跟时间是比较容易找到的
# 1、可以从列表页获取新闻标题、新闻时间
# 2、只能从列表页获取标题
# 通用查找
# 1、给定站定的内容容器。首选是id, 其次是class, 内置Id节点[content, article]
# 2、通过查找是否存在常用的内容节点<article>
# 针对情况1、
# 可以获取时间通过时间获取详情页时间所在节点, 再通过该节点向上回溯内容
# 如果通过时间没有找到内容节点,那么在通过标题找到标题节点。在向上回溯并找到内容节点
# 情况2、
# 通过标题找到标题节点。再向上找到一个包含时间的节点。认为是新闻的时间节点。
# ...
