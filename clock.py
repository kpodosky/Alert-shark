from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

#execute very 30 minutes
@sched.scheduled_job('interval', minutes=30)
def scheduled_job():
#start logic
 sched.start()
