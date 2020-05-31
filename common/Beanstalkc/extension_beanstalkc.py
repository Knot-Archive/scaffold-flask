import collections
import json

# import beanstalkc

from .beanstalkc import Connection  # beanstalk.connection
from .beanstalkc import SocketError  # beanstalk.SocketError
from .beanstalkc import DeadlineSoon

import logging

bean_logger = logging.getLogger('beanstalkc')

MAILBOX = 'mailbox'


class BeanstalkCallback(object):
    def __init__(self, parse):
        self.handlers = collections.defaultdict()
        self.parse = parse

    def register(self, func, solider):
        self.handlers.update({func: solider})

    def work(self, data):
        msg = self.parse(data)
        func = msg.get('func', '')
        args = msg.get('args', [])
        kwargs = msg.get('kwargs', {})
        self.handlers[func](*args, **kwargs)


def default_parse(body):
    return {"func": "default", "args": [], "kwargs": {}}


def default(*args, **kwargs):
    return


class BeanstalkClient:
    def __init__(self):
        self.client = None

    def connect(self, port, host, timeout=60 * 10):
        bean_logger.info(
            "Connection to beanstalk host {}, port {}, timeout {}".format(
                host, port, timeout))
        try:
            self.client = Connection(host=host, port=port, connect_timeout=timeout)
        except  SocketError as e:
            bean_logger.error(
                "Problems connecting to beanstalk host {}, port{}, timeout {}, err msg {}.".format(
                    host, port, timeout, e))
            self.client = None
        return self


class BeanstalkProducer(BeanstalkClient):

    def status(self):
        return self.client.status()

    def put(self, data):
        if not self.client:
            bean_logger.error("No connection")
            return
        jdata = json.dumps(data)
        self.client.put(jdata)


class BeanstalkConsumer(BeanstalkClient):
    def status(self):
        return self.client.status()

    def watch(self, watch):
        self.client.watch(watch)
        return self

    def run(self, callback: BeanstalkCallback, timeout=30):
        if not self.client:
            bean_logger.error("No connection")
            return
        # self.client.watch(watch)
        while True:
            try:
                job = self.client.reserve(timeout=timeout)
            except DeadlineSoon as e:
                bean_logger.error('DeadlineSoon: {}'.format(e))
                job = None
            if not job:
                bean_logger.info("No job.")
                return
            try:
                data = json.loads(job.body)
                res = callback.work(data)
            except Exception as e:
                pass
            finally:
                self.client.delete(job.id)

