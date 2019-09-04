from .parser.board_log import BoardLog


class Abnormal:
    NONE = (0, '正常')

    EMPTY_HOT_NUM = (1, '没有获取到热点信息')  # 链接数为0
    EMPTY_NOT_FOUND = (2, 'item_selector没有配置')

    WARN_HOT_NUM = (20, '获取到的热点数少于预期')
    # ERROR
    ERROR_SOURCE_URL = (10, '热点源连接错误')    # 新闻链接出错
    ERROR_SOURCE_DOC = (11, '热点文档解析错误')

    @classmethod
    def abnoraml(cls, msg):
        return (20, msg)