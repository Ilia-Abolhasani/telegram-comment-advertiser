from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import app.cron.job_explore_channels as job_explore_channels


def start_jobs(context, telegram_api, logger_api):
    scheduler = BackgroundScheduler(
        {'apscheduler.job_defaults.max_instances': 1})

    # job fetch new proxies from other proxy chaneels
    scheduler.add_job(
        lambda: job_explore_channels.start(context, telegram_api, logger_api),
        trigger=CronTrigger.from_crontab('* * * * *')
    )
    scheduler.start()
