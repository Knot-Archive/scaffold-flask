from celery import Celery as _Celery
from werkzeug.local import LocalProxy

"""
https://flask.palletsprojects.com/en/1.1.x/patterns/celery/
"""


class CeleryRQ:
    def __init__(self):
        self.rq = None

    def init_app(self, app):
        celery = _Celery(
            app.import_name,
            backend=app.config['CELERY_RESULT_BACKEND'],
            broker=app.config['CELERY_BROKER_URL']
        )
        celery.conf.update(app.config)

        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery.Task = ContextTask
        self.rq = celery


rq = CeleryRQ()

