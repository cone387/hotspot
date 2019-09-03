import redis
from ..settings import REDIS, REDIS_KEY
import json


class Cookies():
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(**REDIS)
        self.redis_client = redis.StrictRedis(connection_pool=self.redis_pool)
    
    def get_cookies(self, board_id):
        try:
            cookies_str = self.redis_client.hget(REDIS_KEY, board_id)
            cookies_list = json.loads(cookies_str)
            cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}
            return cookies
        except Exception as e:
            print("[%s]get cookies error: %s"%(board_id, str(e)))
            return None
        
    def ping(self):
        self.redis_client.ping()


CookieManager = Cookies()