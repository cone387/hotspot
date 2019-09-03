# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2019-08-31 14:17
# software: PyCharm

from .views import UserView
from django.urls import path, include, re_path


urlpatterns = [
    path('auth/<option>/', UserView.as_view()),

]
