from apscheduler.schedulers.background import BackgroundScheduler
from scheduled_job import address_job

class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    scheduler.add_job(address_job.update_cities, 'interval', minutes=60)
    scheduler.add_job(address_job.update_streets, 'interval', minutes=120)