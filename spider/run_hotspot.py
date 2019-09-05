from hotspot.newscrawler import HotSpotCrawler
from hotspot.parser.manger import ParserManager
from cone.spider_ex.log import spider_logger as logger, formatter, log_console
from hotspot.settings import THREAD_NUM
import logging
import getopt
import sys


def init_logger(logfile):
    # if not sys.platform.startswith('win'):
    #     logger.removeHandler(log_console)
    file_handle = logging.FileHandler(logfile, encoding='utf-8')
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)


if __name__ == "__main__":
    print(sys.argv)
    opts, args = getopt.getopt(sys.argv[1:], "l:t:d:", ["thread=", 'logfile=', 'debug='])
    logfile = "hotspot.log"
    thread_num = THREAD_NUM
    debug = True
    for opt, arg in opts:
        if opt in ('-l', '--logfile'):
            logfile = arg
        elif opt in ('-t', '--thread'):
            thread_num = int(arg)
        if opt in ('-d', '--debug'):
            debug = int(arg) == 1
    print(logfile, debug, thread_num)
    init_logger(logfile)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    parser_manager = ParserManager()
    spider = HotSpotCrawler(parser_manager, thread_num)
    spider.start()