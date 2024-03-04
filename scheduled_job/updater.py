from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from scheduled_job import address_job, mailing

class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    scheduler.add_job(address_job.update_cities, 'interval', minutes=60)
    scheduler.add_job(address_job.update_streets, 'interval', minutes=120)
    scheduler.add_job(mailing.send_message, 'interval', minutes=6)