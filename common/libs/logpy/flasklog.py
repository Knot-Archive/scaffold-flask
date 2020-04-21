from flask import Flask
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import request

server_port = 5000
app = Flask(__name__)
formatter = logging.Formatter("%(asctime)s - %(levelname)-7s - %(message)s")
handler = TimedRotatingFileHandler('log/flask_server.log', when="midnight", interval=1, encoding='utf8')
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

mylogger = logging.getLogger('myapp')
my_formatter = logging.Formatter(
    "[%(asctime)s][%(name)s][%(process)d][%(thread)d][%(message)s][[in %(pathname)s:%(lineno)d]")
my_handler = TimedRotatingFileHandler(
    "log/flask_app.log", when="D", interval=1, backupCount=15,
    encoding="UTF-8", delay=False, utc=True)
app.logger.addHandler(handler)
handler.setFormatter(formatter)
my_handler.setFormatter(my_formatter)
mylogger.setLevel(logging.INFO)
mylogger.addHandler(my_handler)


@app.route('/')
def hello_world():
    mylogger.info('A request happened at %s', 'hello_world')
    mylogger.warning('A warning %s', 'hello_world')
    mylogger.error('An exception occurred at %s', 'hello_world')
    try:
        1 / 0
    except ZeroDivisionError as e:
        mylogger.exception("message")
    return 'Hello, World!'


if __name__ == "__main__":
    app.run('0.0.0.0', port=server_port)
