from news.newscrawler import NewsCrawler, logger
from news.parser.manger import ParserManager
from news import settings

import logging


logger.setLevel(logging.INFO)



if __name__ == "__main__":
    parser_manager = ParserManager()
    spider = NewsCrawler(parser_manager, thread_num=1)
    spider.start()