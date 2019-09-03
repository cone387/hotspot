# status为评论数与最后评论时间的md5
import redis
from ..settings import REDIS
from cone.spider_ex import logger

DAY = 60 * 60 * 24

class _BoardStatus(dict):
    def set_status(self, board_md5: str, status_md5):
        self[board_md5] = status_md5

    def get_status(self, board_md5):
        return self.get(board_md5)

    def different(self, board_md5: str, status_md5):
        old_status = self.get(board_md5)
        if old_status is None:
            return True
        return old_status != status_md5


class _RedisStatus:

    def __init__(self):
        self._redis = redis.Redis(**REDIS)

    def is_different_link(self, board_id, link_md5):
        link_key = f'b_{board_id}_{link_md5}'
        try:
            if self._redis.exists(link_key):
                return False
            self._redis.set(link_key, '')
            self._redis.expire(link_key, DAY * 3)
            return True
        except Exception as e:
            logger.error("redis error: %s", str(e))
            return False

    def is_different_board(self, board_md5):
        board_key = f's_{board_md5}'
        try:
            if self._redis.exists(board_key):
                return False
            self._redis.set(board_key, '')
            self._redis.expire(board_key, DAY * 3)
            return True
        except Exception as e:
            logger.error("redis error: %s", str(e))
            return False




#
# class CrawlStatus(dict):
#     def get_board_status(self, site_md5):
#         status = self.get(site_md5)
#         if status:
#             return BoardStatus(status)
#         self[site_md5] = {}
#         return SiteStatus(self[site_md5])
#
#     def set_site_status(self, site_md5:str, status:dict): # 设置站点的爬取状态
#         self[site_md5] = status
    

# BoardStatus = _BoardStatus()
RedisStatus = _RedisStatus()