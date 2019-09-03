class BoardLog(dict):
    def __init__(self, url='', name='', from_url='', link_num=0, news_link_num=0, news_num=0):
        self.parsed_num = 0
        self.list_doc_error = False
        self.detail_doc_error_num = 0
        self.abnormal = None
        self.warn_msg = None
        self['name'] = name
        self['upload_num'] = 0
        self['last_pubtime'] = '2000-01-01'    # 该板块里的最新发表消息
        self['url'] = url   # 版块URL
        self['link_num'] = link_num # 链接数量
        self['news_link_num'] = news_link_num   # 新闻链接数量
        self['news_num'] = news_num # 新闻数
        self['detail_error_num'] = 0    # 详情页错误数
        # if from_url:
        #     self['from_url'] = from_url # 版块上级url

