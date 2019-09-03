import time


class HotspotLog(dict):

    def __init__(self, source_id=None, ):
        self.url_error = False
        self.doc_error = False
        self['hot_num'] = 0
        self['upload_num'] = 0
        self['collect_num'] = 0
        self['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S')



