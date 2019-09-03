# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2019-08-26 20:02
# software: PyCharm
import sys
import getopt


def get_params():
    params = {'debug': True, 'thread_num': 1}
    opts, _ = getopt.getopt(sys.argv[1:], 't:d:', ['debug=', "thread="])
    for opt, arg in opts:
        if opt in ('-t', '--thread'):
            params['thread_num'] = int(arg)
        elif opt in ('-d', '--debug'):
            params['debug'] = arg == '1'
    return params


StartParams = get_params()
