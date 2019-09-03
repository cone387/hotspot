from .queue import get_dowonload_queue
from cone.tools import get_md5


class Request(dict):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}

    def __init__(self, url=None, callback=None, method='GET', headers=None,
                 cookies=None, meta=None, priority=0, encoding=None,
                 do_filter=False, try_times=3, errorcall=None, **kwargs):
        self.priority = priority
        self.do_filter = do_filter
        self.errorcall = errorcall
        self.meta = meta
        self.method = method
        self.encoding = encoding
        self.callback = callback
        self.done_times = 1
        self['url'] = url
        self['cookies'] = cookies
        self['headers'] = headers or self.headers
        self._fingprint = None
        self.try_times = try_times
        self.update(kwargs)
    
    @property
    def fingprint(self):
        if self._fingprint is None:
            self._fingprint = get_md5(self['url'])
        return self._fingprint

    def start_request(self):
        queue = get_dowonload_queue()
        queue.put(self)

    def __lt__(self, other):
        # priority越小，处理优先级越高
        return self.priority < other.priority


class CrawlerRequest(Request):
    def __init__(self, depth=1, max_depth=2, do_filter=True, **kwargs):
        self.depth = depth
        self.max_depth = max_depth
        super().__init__(do_filter=do_filter, **kwargs)