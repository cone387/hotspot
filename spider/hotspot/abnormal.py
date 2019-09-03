from .parser.board_log import BoardLog


class Abnormal:
    NONE = (0, '正常')

    EMPTY_HOT_NUM = (1, '没有获取到热点信息')  # 链接数为0

    # ERROR
    ERROR_SOURCE_URL = (10, '热点源连接错误')    # 新闻链接出错
    ERROR_SOURCE_DOC = (11, '热点文档解析错误')
