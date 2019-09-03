# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2019-08-26 09:30
# software: PyCharm

from django.urls import path, include
from .api import *

urlpatterns = [
    path('data/website', DataFetcher.as_view()),
    path('config/website/get_next', SpiderSchedule.as_view()),
    path('config/website/enable', get_enable_website),
    path('config/website/crawl_time', get_crawl_time),
    path('config/website/update', update_website)
]
