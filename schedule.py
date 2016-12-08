#!./env/bin/python
from crontab import CronTab

cron  = CronTab(user=True)

job_daily  = cron.new(command='cd ~/canadajob;source env/bin/activate;./daily_task.py',comment='job_daily')

job_daily.every_reboot()

job_daily.enable()

job_hourly = cron.new(command='cd ~/canadajob;source env/bin/activate;./hourly_task.py',comment='job_hourly')

job_hourly.minute.on(0)
job_hourly.hour.during(0,23)
job_hourly.enable()

cron.write()
cron.render()