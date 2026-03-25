from apscheduler.schedulers.background import BackgroundScheduler
import time

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_followup(func, delay_minutes, *args):
    run_time = time.time() + delay_minutes * 60
    scheduler.add_job(func, 'date', run_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(run_time)), args=args)