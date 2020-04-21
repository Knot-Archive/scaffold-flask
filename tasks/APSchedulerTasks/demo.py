from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.events import EVENT_JOB_EXECUTED
from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

jobstores = {
    'mongo': MongoDBJobStore(),
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


def myfunc():
    print("schedual task")


job = scheduler.add_job(myfunc, 'interval', minutes=2, id='my_job_id')
job.modify(max_instances=6, name='Alternate name')


# job.remove()
# scheduler.remove_job('my_job_id')
# scheduler.shutdown()
# scheduler.shutdown(wait=False)
# scheduler.pause()
# scheduler.resume()
# scheduler.start(paused=True)

def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')


scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
