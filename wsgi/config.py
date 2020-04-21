# config.py
import os
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing

debug = True  # todo production switch False
daemon = False  # todo production switch True
loglevel = 'debug'
bind = "0.0.0.0:8001"
pidfile = "log/gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/debug.log"

# 启动的进程数
# workers = multiprocessing.cpu_count()
workers = 2
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'
