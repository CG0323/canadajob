#!./env/bin/python
from crontab import CronTab

cron  = CronTab(user=True)

job_daily = cron.new(command='sudo su; reboot',comment='job_daily')

job_daily.minute.on(0)
job_daily.hour.on(10)
job_daily.enable()

job_reboot  = cron.new(command='cd ~/canadajob;source env/bin/activate;./daily_task.py',comment='job_reboot')

job_reboot.every_reboot()

job_reboot.enable()

job_hourly = cron.new(command='cd ~/canadajob;source env/bin/activate;./hourly_task.py',comment='job_hourly')

job_hourly.minute.on(30)
job_hourly.hour.on(10)
job_hourly.enable()

cron.write()
cron.render()