from .params import StartParams

DEBUG = StartParams.get('debug')
THREAD_NUM = StartParams.get('thread_num')

TASK_FETCH_URL = 'http://47.96.233.65/api/config/website/get_next'
TEST_FETCH_URL = 'http://47.96.233.65/api/config/website/get_next'


MYSQL = {
    'host': '47.94.99.0',
    'db': 'hotspot',
    'user': 'cone',
    'pwd': '3.1415926',
}
COLLECT_LOG_DIR = 'logs'


TABLE = {
    'hotspot': 'data_hotspot',
    'test-hotspot': 'test_data_hotspot',
    'hotspot-source': 'config_source'
}


RUN_LOG_DIR = 'logs'    # 日志

LOG_FILENAME = 'hotspot.collect.log'   # 统计日志存储

CONFIG_REGET_DELAY = 30 # 没有获取到配置时下一次等待该时间再次获取
PROCESS_CONFIG_NUM = 1

print("Run on %s mode"% ("debug" if DEBUG else "release"))
