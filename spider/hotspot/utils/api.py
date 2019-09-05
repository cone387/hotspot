
from ..settings import TASK_FETCH_URL, TEST_FETCH_URL
from cone.spider_ex import logger, Request
import requests
import time


def get_config():
    try:
        value = requests.get(TASK_FETCH_URL, headers=Request.headers, timeout=30).json()['data']
        if not value:
            logger.debug("No more news config")
            # time.sleep(2)
            return get_config()
        return value
    except Exception as e:
        # time.sleep(1)
        logger.debug("Get config error: %s", str(e))
        return get_config()


def get_config_by(id):
    try:
        value = requests.get(TEST_FETCH_URL, params={'id': id}, timeout=30).json()['data']
        if not value:
            return None
        return value
    except Exception as e:
        time.sleep(1)
        logger.debug("Get config error: %s", str(e))
        return None