# from bbs.test import TestSpider

from urllib.request import urlparse, urljoin
import sys
import getopt
from hotspot.test.spider import TestSpider
from hotspot.parser.manger import ParserManager
from cone.tools.timeutil import search_time


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "t:", ["thread="])
    logfile = "news.log"
    thread_num = 3
    for opt, arg in opts:
        if opt in ('-t', '--thread'):
            thread_num = int(arg)
    parser_manager = ParserManager()
    spider = TestSpider(parser_manager, thread_num)
    spider.start()
